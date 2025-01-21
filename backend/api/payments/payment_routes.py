from datetime import datetime, timedelta

import stripe
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user, admin_required
from backend.models import Payment
from backend.schemas.payment_schema import (
    PaymentCreate,
    PaymentOut,
    PaymentVerify,
    PaymentHistory,
    AdminPaymentHistory, PaymentPlatform, PaymentStatus,
)
from backend.models.user import User
from backend.models.subscription_tier import SubscriptionTier
from backend.api.payments.payment_service import (
    create_payment,
    verify_payment,
    get_user_payments,
    get_all_payments,
    refund_payment,
    create_stripe_payment,
    subscribe_to_free_tier,
)
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter()


@router.post("/create", response_model=dict)
def create_payment_route(
    subscription_tier: str = Query(..., description="The subscription tier to purchase"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a Stripe payment session for the selected subscription tier.
    """
    logger.info(f"User {current_user.id} is initiating a payment for subscription tier: {subscription_tier}")

    # Fetch subscription tier
    tier = db.query(SubscriptionTier).filter_by(id=subscription_tier, is_active=True).first()
    if not tier:
        logger.error(f"Invalid or inactive subscription tier: {subscription_tier}")
        raise HTTPException(status_code=400, detail="Invalid subscription tier selected.")

    # Check user's current subscription status
    if current_user.subscription_plan != "Free":
        logger.warning(f"User {current_user.id} is already subscribed to {current_user.subscription_plan}.")
        raise HTTPException(status_code=400, detail="You are already subscribed to a plan.")

    try:
        # Create Stripe session
        payment_session = create_stripe_payment(current_user, tier.id, db)

        # Record payment in the database
        payment_data = PaymentCreate(
            user_id=current_user.id,
            platform=PaymentPlatform.STRIPE,
            amount=tier.price,
            currency=tier.currency,
            subscription_tier_id=tier.id,
            stripe_payment_id=payment_session["session_id"],
        )
        logger.debug(f"Payment Data {payment_data}")
        create_payment(db, payment_data, current_user.id)

        # Increment profile version
        current_user.profile_version += 1
        db.commit()

        logger.info(f"Stripe session created: {payment_session['session_id']} for user {current_user.id}")
        return {"url": payment_session["url"]}
    except Exception as e:
        logger.error(f"Error creating payment session for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create payment session.")


@router.get("/cancel", response_model=dict)
def cancel_payment_route(
    session_id: str = Query(None, description="The Stripe session ID, if available"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Handle cancellation of a payment session when the user chooses to cancel on Stripe's site.
    """
    logger.info(f"Payment cancellation initiated for session ID: {session_id}, user ID: {current_user.id}")

    try:
        if not session_id:
            logger.warning(f"Stripe session ID missing in cancel request for user {current_user.id}")
            raise HTTPException(status_code=400, detail="Missing session ID.")

        # Fetch the payment record in the database
        payment = db.query(Payment).filter(Payment.stripe_payment_id == session_id).first()
        if not payment:
            logger.error(f"No payment record found for session ID: {session_id}")
            raise HTTPException(status_code=404, detail="Payment record not found.")

        # Update the payment status to "cancelled"
        payment.status = PaymentStatus.CANCELLED
        db.commit()
        logger.info(f"Payment status updated to CANCELLED for session ID: {session_id}")

        return {"message": "Payment session has been cancelled successfully."}
    except Exception as e:
        logger.error(f"Error handling payment cancellation for session ID: {session_id}, error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the cancellation.")


@router.post("/verify", response_model=dict)
def verify_payment_route(
    session_id: str = Query(..., description="The Stripe session ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Verify the payment status after Stripe redirects the user back.
    """
    logger.info(f"Verifying payment for session ID: {session_id}, user ID: {current_user.id}")

    try:
        # Fetch the Stripe session
        session = stripe.checkout.Session.retrieve(session_id)
        logger.info(f"Stripe session retrieved: {session.id}, status: {session.payment_status}")

        # Check if payment is already processed in the database
        payment = db.query(Payment).filter_by(stripe_payment_id=session_id).first()
        if not payment:
            logger.error(f"No payment record found for session ID: {session_id}")
            raise HTTPException(status_code=404, detail="Payment record not found.")

        # Handle Stripe statuses
        if session.payment_status == "paid":
            payment.status = PaymentStatus.SUCCESS
            current_user.subscription_plan = payment.subscription_tier.name
            current_user.setup_step = "completed"
            payment.renewal_date = datetime.utcnow() + timedelta(days=30)

            # Increment profile version
            current_user.profile_version += 1
            db.commit()

            logger.info(f"Payment successful for session ID: {session_id}, user ID: {current_user.id}")
            return {"message": "Payment successful!"}
        elif session.payment_status in ["failed", "expired"]:
            payment.status = PaymentStatus.FAILED
            db.commit()
            logger.warning(f"Payment failed for session ID: {session_id}, status: {session.payment_status}")
            return {"message": "Payment failed. Please try again."}
        else:
            logger.warning(f"Unhandled Stripe status: {session.payment_status} for session {session_id}")
            raise HTTPException(
                status_code=400, detail=f"Unhandled payment status: {session.payment_status}"
            )
    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error during verification: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to verify payment.")
    except Exception as e:
        logger.error(f"Error verifying payment for session ID: {session_id}, user ID: {current_user.id}, error: {e}")

        # Attempt recovery if Stripe confirmed success
        payment = db.query(Payment).filter_by(stripe_payment_id=session_id).first()
        if payment and payment.status != PaymentStatus.SUCCESS:
            payment.status = PaymentStatus.SUCCESS
            current_user.subscription_plan = payment.subscription_tier.name
            payment.renewal_date = datetime.utcnow() + timedelta(days=30)
            db.commit()
            logger.info(f"Recovered payment record for session ID {session_id} after error.")
            return {"message": "Payment recovery successful!"}

        raise HTTPException(status_code=500, detail="Failed to verify payment.")


@router.post("/subscribe/free", response_model=dict)
def subscribe_free_tier_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Subscribe the current user to the Free tier.
    """
    try:
        subscribe_to_free_tier(current_user, db)

        # Increment profile version
        current_user.profile_version += 1
        db.commit()

        return {"message": "You have successfully subscribed to the Free tier."}
    except Exception as e:
        logger.error(f"Error subscribing user {current_user.id} to Free tier: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to subscribe to Free tier.")


@router.post("/verify", response_model=PaymentOut)
def verify_payment_status(
    payment_data: PaymentVerify,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Verify the status of a payment with the platform (e.g., Stripe, Google, Apple).
    """
    logger.info(f"User {current_user.id} is verifying payment ID: {payment_data.payment_id}")
    try:
        payment = verify_payment(db, payment_data, current_user.id)
        logger.info(f"Payment verified: {payment.id}, Status: {payment.status}")
        return payment
    except Exception as e:
        logger.error(f"Error verifying payment {payment_data.payment_id} for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to verify payment.")


@router.get("/history", response_model=PaymentHistory)
def get_user_payment_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve the payment history of the current user.
    """
    logger.info(f"Fetching payment history for user {current_user.id}")
    try:
        payments = get_user_payments(current_user.id, page, page_size, db)
        logger.info(f"Fetched {len(payments.payments)} payments for user {current_user.id}")
        return payments
    except Exception as e:
        logger.error(f"Error fetching payment history for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch payment history.")


@router.get("/admin/history", response_model=AdminPaymentHistory, dependencies=[Depends(admin_required)])
def get_all_payment_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Retrieve payment history for all users (admin-only).
    """
    logger.info("Admin is fetching payment history for all users.")
    try:
        payments = get_all_payments(page, page_size, db)
        logger.info(f"Fetched {len(payments.payments)} payments for admin view.")
        return payments
    except Exception as e:
        logger.error(f"Error fetching all payment history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch payment history.")


@router.post("/refund", response_model=PaymentOut, dependencies=[Depends(admin_required)])
def refund_user_payment(
    payment_id: str,
    db: Session = Depends(get_db),
):
    """
    Refund a payment (admin-only).
    """
    logger.info(f"Admin is refunding payment ID: {payment_id}")
    try:
        payment = refund_payment(payment_id, db)
        logger.info(f"Payment refunded: {payment.id}")
        return payment
    except Exception as e:
        logger.error(f"Error refunding payment {payment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to refund payment.")
