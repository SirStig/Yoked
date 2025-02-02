from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import stripe

from backend.core.config import settings
from backend.models.subscription_tier import SubscriptionTier
from backend.models.payment import Payment
from backend.models.user import User
from backend.core.logging_config import get_logger
from backend.schemas.payment_schema import SubscriptionDetails, UpdateSubscription, RefundRequest

logger = get_logger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

### **Retrieve All Subscription Tiers**
def get_all_subscription_tiers(db: Session, include_inactive: bool = False) -> List[SubscriptionTier]:
    """ Retrieve all subscription tiers, ordered by price. """
    try:
        query = db.query(SubscriptionTier).order_by(SubscriptionTier.price.asc())
        if not include_inactive:
            query = query.filter(SubscriptionTier.is_active.is_(True))
        return query.all()
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving subscription tiers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription tiers.")

### **Retrieve a Subscription Tier by ID**
def get_subscription_tier_by_id(db: Session, tier_id: str) -> Optional[SubscriptionTier]:
    """ Retrieve a specific subscription tier by ID. """
    try:
        tier = db.query(SubscriptionTier).filter_by(id=tier_id).first()
        if not tier:
            raise HTTPException(status_code=404, detail="Subscription tier not found.")
        return tier
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription tier.")

### **Create a Subscription Tier (Admin Only)**
def create_subscription_tier(db: Session, tier_data: dict) -> SubscriptionTier:
    """ Create a new subscription tier. """
    try:
        new_tier = SubscriptionTier(**tier_data, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        db.add(new_tier)
        db.commit()
        db.refresh(new_tier)

        new_tier.version = 1
        db.commit()

        logger.info(f"Subscription tier created: {new_tier.name}")
        return new_tier
    except SQLAlchemyError as e:
        logger.error(f"Error creating subscription tier: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create subscription tier.")

### **Update a Subscription Tier (Admin Only)**
def update_subscription_tier(db: Session, tier_id: str, updated_data: dict) -> SubscriptionTier:
    """ Update a subscription tier. """
    try:
        tier = get_subscription_tier_by_id(db, tier_id)
        for key, value in updated_data.items():
            setattr(tier, key, value)
        tier.updated_at = datetime.utcnow()
        tier.version += 1

        db.commit()
        db.refresh(tier)
        return tier
    except SQLAlchemyError as e:
        logger.error(f"Error updating subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update subscription tier.")

### **Deactivate a Subscription Tier (Admin Only)**
def deactivate_subscription_tier(db: Session, tier_id: str) -> None:
    """ Deactivate a subscription tier. """
    try:
        tier = get_subscription_tier_by_id(db, tier_id)
        tier.is_active = False
        tier.updated_at = datetime.utcnow()
        tier.version += 1

        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error deactivating subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to deactivate subscription tier.")

### **Delete a Subscription Tier (Admin Only)**
def delete_subscription_tier(db: Session, tier_id: str) -> None:
    """ Delete a subscription tier if no users are subscribed. """
    try:
        tier = get_subscription_tier_by_id(db, tier_id)
        active_users = db.query(User).filter(User.subscription_plan == tier.name).count()
        if active_users > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete subscription tier with active subscribers. Deactivate it instead."
            )
        db.delete(tier)
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error deleting subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete subscription tier.")

### **Update a User's Subscription (Stripe Integrated)**
def update_user_subscription(user_id: str, subscription_data: UpdateSubscription, db: Session):
    """ Update a user's subscription plan using Stripe. """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        new_subscription = db.query(SubscriptionTier).filter(SubscriptionTier.id == subscription_data.new_plan_id).first()
        if not new_subscription:
            raise HTTPException(status_code=404, detail="Subscription tier not found.")

        # Update subscription via Stripe
        if user.stripe_subscription_id:
            stripe.Subscription.modify(
                user.stripe_subscription_id,
                cancel_at_period_end=False,
                proration_behavior="create_prorations",
                items=[{"id": user.stripe_subscription_item_id, "price": new_subscription.stripe_price_id}],
            )

        user.subscription_plan = new_subscription.name
        user.renewal_date = datetime.utcnow() + timedelta(days=30)

        db.commit()
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error while updating subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update subscription.")
    except SQLAlchemyError as e:
        logger.error(f"Error updating subscription: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update subscription.")

### **Cancel a User's Subscription (Stripe Integrated)**
def cancel_user_subscription(user_id: str, db: Session):
    """ Cancel a user's subscription via Stripe. """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        if user.stripe_subscription_id:
            stripe.Subscription.delete(user.stripe_subscription_id)

        user.subscription_plan = "Free"
        user.renewal_date = None

        db.commit()
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error while cancelling subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription.")
    except SQLAlchemyError as e:
        logger.error(f"Error cancelling subscription: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to cancel subscription.")

### **Process a Refund (Stripe Integrated)**
def process_refund(refund_request: RefundRequest, user_id: str, db: Session):
    """ Process a refund request via Stripe. """
    try:
        payment = db.query(Payment).filter(Payment.id == refund_request.payment_id, Payment.user_id == user_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found.")

        stripe.Refund.create(payment_intent=payment.stripe_payment_id)
        payment.status = "REFUNDED"
        db.commit()
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error while processing refund: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process refund.")
    except SQLAlchemyError as e:
        logger.error(f"Error processing refund: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to process refund.")
