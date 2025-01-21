from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from backend.core.logging_config import get_logger
from backend.core.config import settings
from backend.models.payment import Payment, PaymentStatus
from backend.models.user import User
from backend.core.database import get_db
import stripe

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
        logger.error("Invalid payload received")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid Stripe signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    except Exception as e:
        logger.error(f"Unexpected error during webhook verification: {e}")
        raise HTTPException(status_code=500, detail="Unexpected verification error")

    # Log the event type and ID
    event_id = event.get("id", "unknown")
    event_type = event.get("type", "unknown")
    logger.info(f"Received Stripe event: {event_type} (ID: {event_id})")

    event_data = event.get("data", {}).get("object", {})
    if not event_data:
        logger.warning(f"No event data found for event {event_id}")
        return {"message": "Webhook received, no actionable data"}

    try:
        if event_type == "checkout.session.completed":
            handle_checkout_session_completed(event_data, db)
        elif event_type == "invoice.payment_succeeded":
            handle_payment_success(event_data, db)
        elif event_type == "invoice.payment_failed":
            handle_payment_failure(event_data, db)
        elif event_type == "checkout.session.expired":
            handle_checkout_session_expired(event_data, db)
        elif event_type == "customer.subscription.updated":
            handle_subscription_updated(event_data, db)
        elif event_type == "customer.subscription.deleted":
            handle_subscription_deleted(event_data, db)
        else:
            logger.warning(f"Unhandled event type: {event_type}")
    except Exception as e:
        logger.error(f"Error processing event {event_type} (ID: {event_id}): {e}")
        raise HTTPException(status_code=500, detail=f"Error processing event: {event_type}")

    return {"message": "Webhook processed successfully"}


# Event Handlers
def handle_checkout_session_completed(session, db: Session):
    stripe_payment_id = session.get("id")
    customer_email = session.get("customer_email")
    logger.info(f"Checkout session completed for {stripe_payment_id}")

    user = db.query(User).filter(User.email == customer_email).first()
    if not user:
        logger.error(f"No user found with email {customer_email}")
        return

    payment = db.query(Payment).filter(Payment.stripe_payment_id == stripe_payment_id).first()
    if payment:
        if payment.status == PaymentStatus.SUCCESS:
            logger.info(f"Payment {payment.id} already processed successfully.")
            return

        payment.status = PaymentStatus.SUCCESS
        payment.renewal_date = datetime.utcnow() + timedelta(days=30)
        user.subscription_plan = payment.subscription_tier.name
        db.commit()
        logger.info(f"Recovered and updated payment record for user {user.id}.")
    else:
        logger.warning(f"No payment record found for Stripe session ID {stripe_payment_id}.")

def handle_payment_success(invoice, db: Session):
    stripe_subscription_id = invoice.get("subscription")
    logger.info(f"Payment succeeded for subscription {stripe_subscription_id}")

    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.SUCCESS
        payment.renewal_date = datetime.utcnow() + timedelta(days=30)
        db.commit()
        logger.info(f"Subscription renewed for payment ID {payment.id}")


def handle_payment_failure(invoice, db: Session):
    stripe_subscription_id = invoice.get("subscription")
    logger.warning(f"Payment failed for subscription {stripe_subscription_id}")

    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.FAILED
        db.commit()
        logger.warning(f"Payment marked as failed for payment ID {payment.id}")

def handle_checkout_session_expired(session, db: Session):
    stripe_payment_id = session.get("id")
    logger.info(f"Checkout session expired for {stripe_payment_id}")

    payment = db.query(Payment).filter(Payment.stripe_payment_id == stripe_payment_id).first()
    if payment:
        payment.status = PaymentStatus.FAILED
        db.commit()
        logger.info(f"Expired payment marked as FAILED for payment ID {payment.id}")

def handle_subscription_updated(subscription, db: Session):
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
    stripe_subscription_id = subscription.get("id")
    logger.warning(f"Subscription deleted: {stripe_subscription_id}")

    payment = db.query(Payment).filter(Payment.stripe_subscription_id == stripe_subscription_id).first()
    if payment:
        payment.status = PaymentStatus.CANCELLED
        db.commit()
        logger.warning(f"Subscription cancelled for payment ID {payment.id}")
