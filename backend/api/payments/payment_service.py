import uuid
from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import stripe

from backend.core.logging_config import get_logger
from backend.models import SubscriptionTier
from backend.models.payment import Payment, PaymentPlatform, PaymentStatus
from backend.models.user import User
from backend.schemas.payment_schema import PaymentCreate, PaymentVerify, PaymentHistory, AdminPaymentHistory
from backend.core.config import settings

logger = get_logger(__name__)

# Initialize Stripe API
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment(user: User, subscription_tier_id: str, db: Session) -> dict:
    """
    Creates a Stripe Checkout session for a user based on subscription tier ID.
    """
    logger.info(f"Creating Stripe payment for user {user.id}, subscription tier ID: {subscription_tier_id}")
    try:
        # Fetch the subscription tier
        tier = db.query(SubscriptionTier).filter_by(id=subscription_tier_id).first()
        if not tier:
            logger.error(f"Subscription tier {subscription_tier_id} not found.")
            raise ValueError(f"Invalid subscription tier ID: {subscription_tier_id}")

        # Validate tier details
        if not tier.price or not tier.currency or not tier.recurring_interval:
            logger.error(
                f"Subscription tier {tier.name} is missing required fields (price, currency, interval)."
            )
            raise ValueError(f"Invalid details for subscription tier: {tier.name}")

        # Map recurring interval to Stripe-compatible format
        interval_map = {
            "monthly": "month",
            "yearly": "year",
            "daily": "day",
            "weekly": "week",
        }
        stripe_interval = interval_map.get(tier.recurring_interval.lower())
        if not stripe_interval:
            logger.error(f"Invalid recurring interval: {tier.recurring_interval} for tier {tier.name}")
            raise ValueError(f"Invalid interval for subscription tier: {tier.name}")

        # Construct product description with tier features
        feature_list = "\n".join(
            [f"- {feature}" for feature in tier.features]) if tier.features else "No features listed"
        product_description = (
            f"{tier.name} subscription includes:\n"
            f"{feature_list}\n\n"
            f"Billing cycle: {tier.billing_cycle}\n"
            f"Cancellation policy: {tier.cancellation_policy}"
        )

        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": tier.currency.lower(),
                    "product_data": {
                        "name": tier.name,
                        "description": product_description,
                        "metadata": {
                            "tier_id": str(tier.id),
                            "billing_cycle": tier.billing_cycle,
                            "cancellation_policy": tier.cancellation_policy,
                            "max_reel_uploads": tier.max_reel_uploads,
                            "max_saved_workouts": tier.max_saved_workouts,
                            "max_messages_per_day": tier.max_messages_per_day,
                        },
                    },
                    "unit_amount": tier.price,
                    "recurring": {"interval": stripe_interval},
                },
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{settings.FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/cancel?session_id={{CHECKOUT_SESSION_ID}}",
            metadata={
                "user_id": str(user.id),
                "user_email": user.email,
            },
        )

        logger.info(f"Stripe session created: {session.id}")
        return {"session_id": session.id, "url": session.url}
    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create Stripe payment session.")
    except Exception as e:
        logger.error(f"Error creating Stripe session: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the payment session.")


def subscribe_to_free_tier(user: User, db: Session) -> None:
    """
    Subscribes a user to the Free tier and updates their setup step to completed.
    """
    logger.info(f"Subscribing user {user.id} to Free tier")
    try:
        user.subscription_plan = "Free"
        user.setup_step = "completed"

        # Increment profile version
        user.profile_version += 1
        db.commit()

        logger.info(f"User {user.id} successfully subscribed to Free tier")
    except SQLAlchemyError as e:
        logger.error(f"Database error subscribing user {user.id} to Free tier: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to subscribe to Free tier")


def create_payment(db: Session, payment_data: PaymentCreate, user_id: UUID) -> Payment:
    logger.info(f"Creating payment for user ID: {user_id} with data: {payment_data}")
    try:
        new_payment = Payment(
            id=uuid.uuid4(),
            user_id=user_id,
            stripe_payment_id=payment_data.stripe_payment_id,
            google_payment_id=payment_data.google_payment_id,
            apple_payment_id=payment_data.apple_payment_id,
            platform=payment_data.platform.value,
            amount=payment_data.amount,
            currency=payment_data.currency,
            subscription_tier_id=payment_data.subscription_tier_id,
            renewal_date=payment_data.renewal_date,
            status=PaymentStatus.PENDING.value.upper(),
            timestamp=datetime.utcnow(),
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        # Increment profile version
        user = db.query(User).filter(User.id == user_id).first()
        user.profile_version += 1
        db.commit()

        logger.info(f"Payment created successfully with ID: {new_payment.id}")
        return new_payment
    except Exception as e:
        logger.error(f"Failed to create payment for user ID: {user_id}, error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create payment record")


def verify_payment(
        db: Session,
        payment_verify: PaymentVerify,
        user_id: uuid.UUID
) -> Payment:
    """
    Verify the status of a payment based on its platform-specific ID
    and update the user's setup_step if successful.
    """
    logger.info(f"Verifying payment for user ID: {user_id} with data: {payment_verify}")
    payment = db.query(Payment).filter(
        Payment.user_id == user_id,
        Payment.id == payment_verify.payment_id
    ).first()

    if not payment:
        logger.error(f"Payment record not found for ID: {payment_verify.payment_id}")
        raise HTTPException(status_code=404, detail="Payment record not found")

    # Verify payment status
    if payment.platform == PaymentPlatform.STRIPE:
        try:
            stripe_payment = stripe.PaymentIntent.retrieve(payment_verify.payment_id)
            payment.status = (
                PaymentStatus.SUCCESS if stripe_payment["status"] == "succeeded" else PaymentStatus.FAILED
            )
        except stripe.error.StripeError as e:
            logger.error(f"Stripe verification error: {str(e)}")
            raise HTTPException(status_code=500, detail="Payment verification failed")

    db.commit()
    db.refresh(payment)

    if payment.status == PaymentStatus.SUCCESS:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User not found for ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        user.setup_step = "completed"

        # Increment profile version
        user.profile_version += 1
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_id}'s setup_step updated to 'completed'")

    return payment


def refund_payment(payment_id: str, db: Session) -> Payment:
    """
    Refund a payment and update the status in the database (admin-only).
    """
    logger.info(f"Processing refund for payment ID: {payment_id}")
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            logger.error(f"Payment not found for ID: {payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found")

        if payment.status != PaymentStatus.SUCCESS:
            raise HTTPException(status_code=400, detail="Only successful payments can be refunded.")

        if payment.platform == PaymentPlatform.STRIPE:
            stripe.Refund.create(payment_intent=payment.stripe_payment_id)
        payment.status = PaymentStatus.FAILED  # Marking as refunded
        db.commit()
        db.refresh(payment)
        logger.info(f"Payment refunded successfully: {payment.id}")
        return payment
    except SQLAlchemyError as e:
        logger.error(f"Error refunding payment ID {payment_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error processing refund")


def get_user_payments(
        user_id: uuid.UUID, page: int, page_size: int, db: Session
) -> PaymentHistory:
    """
    Fetch paginated payment history for a user.
    """
    logger.info(f"Fetching payment history for user ID: {user_id}")
    try:
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
            payments=[payment for payment in payments],
        )
    except SQLAlchemyError as e:
        logger.error(f"Error fetching payments for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching payment history")


def get_all_payments(page: int, page_size: int, db: Session) -> AdminPaymentHistory:
    """
    Fetch paginated payment history for all users (admin-only).
    """
    logger.info("Fetching all payment history for admin.")
    try:
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
            payments=[payment for payment in payments],
        )
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all payments: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching payment records")
