from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Request, Depends
from backend.core.logging_config import get_logger
from backend.core.config import settings
from backend.models.payment import Payment, PaymentStatus
from backend.models.user import User
from sqlalchemy.orm import Session
from backend.core.database import get_db
import stripe
import json

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter()

@router.post("/", response_model=None)
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Stripe webhook handler to process events sent by Stripe.
    """
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid Stripe signature")
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")

    # Process Stripe events
    event_type = event["type"]
    event_data = event["data"]["object"]

    logger.info(f"Processing Stripe event: {event_type}")

    try:
        if event_type == "checkout.session.completed":
            handle_checkout_session_completed(event_data, db)
        elif event_type == "invoice.payment_succeeded":
            handle_payment_success(event_data, db)
        elif event_type == "invoice.payment_failed":
            handle_payment_failure(event_data, db)
        elif event_type == "customer.subscription.updated":
            handle_subscription_updated(event_data, db)
        elif event_type == "customer.subscription.deleted":
            handle_subscription_deleted(event_data, db)
        else:
            logger.warning(f"Unhandled event type: {event_type}")
    except Exception as e:
        logger.error(f"Error processing event {event_type}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing event: {event_type}")

    return {"message": "Webhook processed successfully"}

# Additional Handlers
def handle_subscription_updated(subscription, db: Session):
    """
    Handle subscription updates (e.g., changes to the plan or status).
    """
    stripe_subscription_id = subscription.get("id")
    status = subscription.get("status")
    logger.info(f"Subscription updated: {stripe_subscription_id}, status: {status}")

    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.SUCCESS if status == "active" else PaymentStatus.FAILED
        payment.renewal_date = datetime.utcnow() + timedelta(days=30) if status == "active" else None
        db.commit()
        logger.info(f"Subscription updated in database for payment ID {payment.id}")

def handle_subscription_deleted(subscription, db: Session):
    """
    Handle subscription cancellations or deletions.
    """
    stripe_subscription_id = subscription.get("id")
    logger.warning(f"Subscription deleted: {stripe_subscription_id}")

    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.CANCELLED
        db.commit()
        logger.warning(f"Subscription cancelled for payment ID {payment.id}")



def handle_checkout_session_completed(session, db: Session):
    """
    Handle successful checkout sessions from Stripe.
    """
    stripe_payment_id = session.get("id")
    customer_email = session.get("customer_email")
    logger.info(f"Checkout session completed for {stripe_payment_id}")

    # Fetch user by email
    user = db.query(User).filter(User.email == customer_email).first()
    if not user:
        logger.error(f"No user found with email {customer_email}")
        return

    # Update payment record in database
    payment = db.query(Payment).filter(Payment.stripe_payment_id == stripe_payment_id).first()
    if payment:
        payment.status = PaymentStatus.SUCCESS
        db.commit()
        logger.info(f"Payment record updated for user {user.id}")


def handle_payment_success(invoice, db: Session):
    """
    Handle successful invoice payments.
    """
    stripe_subscription_id = invoice.get("subscription")
    logger.info(f"Payment succeeded for subscription {stripe_subscription_id}")

    # Update user's subscription status
    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.SUCCESS
        payment.renewal_date = datetime.utcnow() + timedelta(days=30)  # Example: monthly renewal
        db.commit()
        logger.info(f"Subscription renewed for payment ID {payment.id}")


def handle_payment_failure(invoice, db: Session):
    """
    Handle failed invoice payments.
    """
    stripe_subscription_id = invoice.get("subscription")
    logger.warning(f"Payment failed for subscription {stripe_subscription_id}")

    # Update user's subscription status
    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.FAILED
        db.commit()
        logger.warning(f"Payment marked as failed for payment ID {payment.id}")
