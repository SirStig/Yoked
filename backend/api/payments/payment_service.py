import uuid
from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import stripe

from backend.core.logging_config import get_logger
from backend.models.subscription_tier import SubscriptionTier
from backend.models.payment import Payment, PaymentPlatform, PaymentStatus
from backend.models.user import User
from backend.schemas.payment_schema import PaymentCreate, PaymentVerify, PaymentHistory, AdminPaymentHistory
from backend.core.config import settings

logger = get_logger(__name__)

# Initialize Stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(user: User, subscription_tier_id: str, db: Session) -> dict:
    """Creates a Stripe Checkout session for a user based on subscription tier ID."""
    try:
        logger.info(f"Creating Stripe payment for user {user.id}, subscription tier ID: {subscription_tier_id}")

        tier = db.query(SubscriptionTier).filter_by(id=subscription_tier_id, is_active=True).first()
        if not tier:
            raise HTTPException(status_code=400, detail="Invalid subscription tier selected.")

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": tier.currency.lower(),
                    "product_data": {"name": tier.name},
                    "unit_amount": tier.price,
                    "recurring": {"interval": tier.recurring_interval},
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{settings.FRONTEND_URL}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/payment-cancel?session_id={{CHECKOUT_SESSION_ID}}",
            metadata={"user_id": str(user.id), "tier_id": str(tier.id)}
        )

        logger.info(f"Stripe session created: {stripe_session.id} for user {user.id}")
        return {"session_id": stripe_session.id, "url": stripe_session.url}

    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create Stripe payment session.")
    except Exception as e:
        logger.error(f"Unexpected error while creating payment session: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the payment session.")


def subscribe_to_free_tier(user: User, db: Session):
    """Subscribes a user to the Free tier and updates their setup step to completed."""
    try:
        logger.info(f"Subscribing user {user.id} to Free tier")

        user.subscription_plan = "Free"
        user.setup_step = "completed"
        user.profile_version += 1
        db.commit()

        logger.info(f"User {user.id} successfully subscribed to Free tier")
    except SQLAlchemyError as e:
        logger.error(f"Database error subscribing user {user.id} to Free tier: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to subscribe to Free tier.")


def create_payment(db: Session, payment_data: PaymentCreate, user_id: uuid.UUID) -> Payment:
    """Creates a new payment record in the database."""
    try:
        logger.info(f"Creating payment for user ID: {user_id} with data: {payment_data}")

        new_payment = Payment(
            id=uuid.uuid4(),
            user_id=user_id,
            stripe_payment_id=payment_data.stripe_payment_id,
            platform=payment_data.platform.value,
            amount=payment_data.amount,
            currency=payment_data.currency,
            subscription_tier_id=payment_data.subscription_id,
            renewal_date=payment_data.renewal_date,
            status=PaymentStatus.PENDING.value,
            timestamp=datetime.utcnow(),
        )

        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        # Update profile version
        user = db.query(User).filter(User.id == user_id).first()
        user.profile_version += 1
        db.commit()

        logger.info(f"Payment created successfully: {new_payment.id}")
        return new_payment
    except SQLAlchemyError as e:
        logger.error(f"Failed to create payment for user ID: {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create payment record.")


def verify_payment(db: Session, payment_verify: PaymentVerify, user_id: uuid.UUID) -> Payment:
    """Verify the status of a payment and update user's subscription if successful."""
    try:
        logger.info(f"Verifying payment for user ID: {user_id} with data: {payment_verify}")

        payment = db.query(Payment).filter(Payment.id == payment_verify.payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found.")

        if payment.platform == PaymentPlatform.STRIPE:
            stripe_payment = stripe.PaymentIntent.retrieve(payment_verify.payment_id)
            payment.status = (
                PaymentStatus.SUCCESS if stripe_payment["status"] == "succeeded" else PaymentStatus.FAILED
            )

        db.commit()
        db.refresh(payment)

        if payment.status == PaymentStatus.SUCCESS:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            user.setup_step = "completed"
            user.profile_version += 1
            db.commit()

            logger.info(f"User {user_id}'s setup_step updated to 'completed'")

        return payment
    except stripe.error.StripeError as e:
        logger.error(f"Stripe verification error: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment verification failed.")
    except SQLAlchemyError as e:
        logger.error(f"Database error verifying payment: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to verify payment.")
    except Exception as e:
        logger.error(f"Unexpected error in payment verification: {str(e)}")
        raise HTTPException(status_code=500, detail="Payment verification failed.")


def get_user_payments(user_id: uuid.UUID, page: int, page_size: int, db: Session) -> PaymentHistory:
    """Fetch paginated payment history for a user."""
    try:
        logger.info(f"Fetching payment history for user ID: {user_id}")

        payments_query = db.query(Payment).filter(Payment.user_id == user_id)
        total_payments = payments_query.count()
        payments = (
            payments_query.order_by(Payment.timestamp.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return PaymentHistory(
            total=total_payments,
            payments=payments
        )
    except SQLAlchemyError as e:
        logger.error(f"Error fetching payments for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching payment history.")


def get_all_payments(page: int, page_size: int, db: Session) -> AdminPaymentHistory:
    """Fetch paginated payment history for all users (admin-only)."""
    try:
        logger.info("Fetching all payment history for admin.")

        payments_query = db.query(Payment)
        total_payments = payments_query.count()
        payments = (
            payments_query.order_by(Payment.timestamp.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return AdminPaymentHistory(
            total=total_payments,
            payments=payments
        )
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all payments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching payment records.")
