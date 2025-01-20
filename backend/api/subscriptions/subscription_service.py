from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from backend.models.subscription_tier import SubscriptionTier
from backend.models.user import User
from backend.core.logging_config import get_logger

logger = get_logger(__name__)

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
        logger.info(f"Subscription tier deleted: {tier.name}")
    except SQLAlchemyError as e:
        logger.error(f"Error deleting subscription tier {tier_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete subscription tier.")
