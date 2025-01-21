from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.core.database import SessionLocal
from backend.models.payment import Payment, PaymentStatus
from backend.models.session import Session as UserSession
from backend.core.logging_config import get_logger
import stripe
from backend.core.config import settings
from backend.tasks.celery_app import celery_app

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Logger setup
logger = get_logger(__name__)

@celery_app.task
def cleanup_expired_sessions():
    """
    Remove expired sessions from the database.
    """
    db = SessionLocal()
    try:
        logger.info("Cleaning up expired sessions...")
        expired_count = db.query(UserSession).filter(
            UserSession.expires_at < datetime.utcnow()
        ).delete()
        db.commit()
        logger.info(f"Removed {expired_count} expired sessions.")
    except SQLAlchemyError as e:
        logger.error(f"Error cleaning up expired sessions: {str(e)}")
        db.rollback()
    finally:
        db.close()

@celery_app.task
def cleanup_pending_payments():
    """
    Mark long-pending payments as failed.
    """
    db = SessionLocal()
    try:
        expiration_time = datetime.utcnow() - timedelta(hours=1)  # Example: 1-hour expiration
        pending_payments = db.query(Payment).filter(
            Payment.status == PaymentStatus.PENDING,
            Payment.timestamp < expiration_time
        ).all()

        for payment in pending_payments:
            logger.info(f"Marking payment {payment.id} as failed (expired).")
            payment.status = PaymentStatus.FAILED
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error during pending payment cleanup: {str(e)}")
        db.rollback()
    finally:
        db.close()

@celery_app.task
def cleanup_expired_subscriptions():
    """
    Mark subscriptions past their renewal date as inactive.
    """
    db = SessionLocal()
    try:
        logger.info("Cleaning up expired subscriptions...")
        expired_subscriptions = db.query(Payment).filter(
            Payment.status == PaymentStatus.SUCCESS,
            Payment.renewal_date < datetime.utcnow()
        ).all()

        for subscription in expired_subscriptions:
            logger.info(f"Marking subscription {subscription.id} as expired.")
            subscription.status = PaymentStatus.FAILED
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error during subscription cleanup: {str(e)}")
        db.rollback()
    finally:
        db.close()

@celery_app.task
def validate_with_stripe():
    """
    Verify the status of incomplete payments or subscriptions with Stripe.
    """
    db = SessionLocal()
    try:
        logger.info("Validating pending payments with Stripe...")
        incomplete_payments = db.query(Payment).filter(
            Payment.status == PaymentStatus.PENDING
        ).all()

        for payment in incomplete_payments:
            try:
                # Verify the session with Stripe
                stripe_session = stripe.checkout.Session.retrieve(payment.stripe_payment_id)
                if stripe_session.payment_status == "paid":
                    logger.info(f"Payment {payment.id} marked as successful (Stripe confirmed).")
                    payment.status = PaymentStatus.SUCCESS
                elif stripe_session.payment_status in ["failed", "expired"]:
                    logger.info(f"Payment {payment.id} marked as failed (Stripe confirmed).")
                    payment.status = PaymentStatus.FAILED
                db.commit()
            except stripe.error.StripeError as e:
                logger.error(f"Stripe API error while validating payment {payment.id}: {str(e)}")
    except SQLAlchemyError as e:
        logger.error(f"Database error during Stripe validation: {str(e)}")
        db.rollback()
    finally:
        db.close()

@celery_app.task
def cleanup_unused_data():
    """
    Placeholder for cleaning up any additional temporary or unused data.
    """
    db = SessionLocal()
    try:
        logger.info("Cleaning up unused data (if any)...")
        # Example: Add custom logic here for cleaning unused or temporary data
        logger.info("No unused data cleanup implemented yet.")
    except Exception as e:
        logger.error(f"Error cleaning up unused data: {str(e)}")
    finally:
        db.close()
