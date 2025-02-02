from datetime import datetime, timedelta
import stripe
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user, admin_required
from backend.models.payment import Payment
from backend.schemas.payment_schema import (
    PaymentCreate,
    PaymentOut,
    PaymentVerify,
    PaymentHistory,
    AdminPaymentHistory,
    PaymentPlatform,
    PaymentStatus,
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
    try:
        logger.info(f"User {current_user.id} initiating a payment for subscription tier: {subscription_tier}")

        # Fetch subscription tier
        tier = db.query(SubscriptionTier).filter_by(id=subscription_tier, is_active=True).first()
        if not tier:
            logger.error(f"Invalid or inactive subscription tier: {subscription_tier}")
            raise HTTPException(status_code=400, detail="Invalid subscription tier selected.")

        # Check if user is already subscribed
        if current_user.subscription_plan != "Free":
            logger.warning(f"User {current_user.id} already subscribed to {current_user.subscription_plan}.")
            raise HTTPException(status_code=400, detail="You are already subscribed to a plan.")

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


@router.post("/verify", response_model=PaymentOut)
def verify_payment_status(
        payment_data: PaymentVerify,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    """
    Verify the status of a payment with the platform (e.g., Stripe, Google, Apple).
    """
    try:
        logger.info(f"User {current_user.id} verifying payment ID: {payment_data.payment_id}")
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
    try:
        logger.info(f"Fetching payment history for user {current_user.id}")
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
    try:
        logger.info("Admin fetching payment history for all users.")
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
    try:
        logger.info(f"Admin refunding payment ID: {payment_id}")
        payment = refund_payment(payment_id, db)
        logger.info(f"Payment refunded: {payment.id}")
        return payment

    except Exception as e:
        logger.error(f"Error refunding payment {payment_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to refund payment.")
