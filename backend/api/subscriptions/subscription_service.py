from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from backend.core.config import settings
from backend.models.subscription_tier import SubscriptionTier
from backend.models.user import User
from backend.core.logging_config import get_logger
from backend.schemas.subscription_tier_schema import SubscriptionDetails, UpdateSubscription
import stripe

logger = get_logger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_all_subscription_tiers(db: Session, include_inactive: bool = False) -> List[SubscriptionTier]:
    """
    Retrieve all subscription tiers, ordered by price (ascending).
    :param db: Database session.
    :param include_inactive: Whether to include inactive subscription tiers.
    :return: List of subscription tiers.
    """
    try:
        query = db.query(SubscriptionTier).order_by(SubscriptionTier.price.asc())  # Order by price ascending
        if not include_inactive:
            query = query.filter(SubscriptionTier.is_active.is_(True))
        tiers = query.all()
        logger.debug(f"Fetched subscription tiers: {tiers}")
        return tiers
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving subscription tiers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription tiers.")

def get_subscription_tier_by_id(db: Session, tier_id: str) -> Optional[SubscriptionTier]:
    """
    Retrieve a subscription tier by its ID.
    :param db: Database session.
    :param tier_id: ID of the subscription tier.
    :return: Subscription tier or None.
    """
    try:
        tier = db.query(SubscriptionTier).filter_by(id=tier_id).first()
        if not tier:
            raise HTTPException(status_code=404, detail="Subscription tier not found.")
        return tier
    except SQLAlchemyError as e:
        logger.error(f"Error retrieving subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription tier.")

def create_subscription_tier(db: Session, tier_data: dict) -> SubscriptionTier:
    """
    Create a new subscription tier.
    :param db: Database session.
    :param tier_data: Dictionary containing subscription tier details.
    :return: Created subscription tier.
    """
    try:
        new_tier = SubscriptionTier(**tier_data, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        db.add(new_tier)
        db.commit()
        db.refresh(new_tier)

        # Increment version after creation
        new_tier.version = 1
        db.commit()

        logger.info(f"Subscription tier created: {new_tier.name}")
        return new_tier
    except SQLAlchemyError as e:
        logger.error(f"Error creating subscription tier: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create subscription tier.")

def update_subscription_tier(db: Session, tier_id: str, updated_data: dict) -> SubscriptionTier:
    """
    Update a subscription tier.
    :param db: Database session.
    :param tier_id: ID of the subscription tier.
    :param updated_data: Dictionary containing updated subscription tier details.
    :return: Updated subscription tier.
    """
    try:
        tier = get_subscription_tier_by_id(db, tier_id)
        for key, value in updated_data.items():
            setattr(tier, key, value)
        tier.updated_at = datetime.utcnow()

        # Increment the version
        tier.version += 1
        logger.debug(f"Incremented version for subscription tier {tier_id} to {tier.version}")

        db.commit()
        db.refresh(tier)
        logger.info(f"Subscription tier updated: {tier.name}")
        return tier
    except SQLAlchemyError as e:
        logger.error(f"Error updating subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update subscription tier.")

def deactivate_subscription_tier(db: Session, tier_id: str) -> None:
    """
    Deactivate a subscription tier (set is_active to False).
    :param db: Database session.
    :param tier_id: ID of the subscription tier.
    """
    try:
        tier = get_subscription_tier_by_id(db, tier_id)
        tier.is_active = False
        tier.updated_at = datetime.utcnow()

        # Increment the version
        tier.version += 1
        logger.debug(f"Incremented version for subscription tier {tier_id} to {tier.version}")

        db.commit()
        logger.info(f"Subscription tier deactivated: {tier.name}")
    except SQLAlchemyError as e:
        logger.error(f"Error deactivating subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to deactivate subscription tier.")

def delete_subscription_tier(db: Session, tier_id: str) -> None:
    """
    Delete a subscription tier if no users are subscribed to it.
    :param db: Database session.
    :param tier_id: ID of the subscription tier.
    """
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

        # Increment the version upon deletion
        db.commit()

        logger.info(f"Subscription tier deleted: {tier.name}")
    except SQLAlchemyError as e:
        logger.error(f"Error deleting subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete subscription tier.")


def get_user_subscription_details(user_id: str, db: Session) -> SubscriptionDetails:
    """
    Fetch subscription details for a specific user.
    :param user_id: ID of the user.
    :param db: Database session.
    :return: Subscription details.
    """
    logger.info(f"Fetching subscription details for user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        subscription = db.query(SubscriptionTier).filter(SubscriptionTier.name == user.subscription_plan).first()
        if not subscription:
            logger.warning(f"Subscription tier not found for user ID {user_id}")
            raise HTTPException(status_code=404, detail="Subscription tier not found")

        return SubscriptionDetails(
            subscription_name=subscription.name,
            price=subscription.price,
            currency=subscription.currency,
            status="Active" if subscription.is_active else "Inactive",
            renewal_date=user.renewal_date,
        )
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch subscription details for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscription details")

def update_user_subscription(user_id: str, subscription_data: UpdateSubscription, db: Session):
    """
    Update a user's subscription plan with Stripe integration.
    :param user_id: ID of the user.
    :param subscription_data: Updated subscription details.
    :param db: Database session.
    """
    logger.info(f"Updating subscription for user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        new_subscription = db.query(SubscriptionTier).filter(SubscriptionTier.id == subscription_data.subscription_tier_id).first()
        if not new_subscription:
            logger.warning(f"Subscription tier not found: {subscription_data.subscription_tier_id}")
            raise HTTPException(status_code=404, detail="Subscription tier not found")

        # Update Stripe subscription if user has a Stripe customer ID
        if user.stripe_customer_id:
            stripe.Subscription.modify(
                user.stripe_subscription_id,
                items=[
                    {
                        "id": user.stripe_subscription_item_id,
                        "price": new_subscription.stripe_price_id,
                    }
                ],
            )

        user.subscription_plan = new_subscription.name
        user.renewal_date = datetime.utcnow() + timedelta(days=30)  # Example renewal period

        db.commit()
        logger.info(f"Subscription updated successfully for user ID {user_id}")
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error while updating subscription for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update subscription in Stripe")
    except SQLAlchemyError as e:
        logger.error(f"Failed to update subscription for user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update subscription")

def cancel_user_subscription(user_id: str, db: Session):
    """
    Cancel a user's subscription with Stripe integration.
    :param user_id: ID of the user.
    :param db: Database session.
    """
    logger.info(f"Cancelling subscription for user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        # Cancel Stripe subscription if user has a Stripe subscription ID
        if user.stripe_subscription_id:
            stripe.Subscription.delete(user.stripe_subscription_id)

        user.subscription_plan = "Free"
        user.renewal_date = None

        db.commit()
        logger.info(f"Subscription cancelled successfully for user ID {user_id}")
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error while cancelling subscription for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription in Stripe")
    except SQLAlchemyError as e:
        logger.error(f"Failed to cancel subscription for user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to cancel subscription")

