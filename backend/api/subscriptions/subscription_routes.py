from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.core.database import get_db
from backend.api.auth.auth_service import admin_required
from backend.schemas.payment_schema import SubscriptionTierBase, SubscriptionTierOut
from backend.api.subscriptions.subscription_service import (
    get_all_subscription_tiers,
    get_subscription_tier_by_id,
    create_subscription_tier,
    update_subscription_tier,
    deactivate_subscription_tier,
    delete_subscription_tier,
)
from backend.core.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[SubscriptionTierOut])
def list_subscription_tiers(
    include_inactive: bool = Query(False, description="Include inactive subscription tiers in the response"),
    db: Session = Depends(get_db),
):
    """
    List all subscription tiers.
    """
    try:
        logger.info("Listing subscription tiers.")
        tiers = get_all_subscription_tiers(db, include_inactive)
        return tiers
    except Exception as e:
        logger.error(f"Error listing subscription tiers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list subscription tiers.")


@router.get("/{tier_id}", response_model=SubscriptionTierOut)
def retrieve_subscription_tier(
    tier_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve a specific subscription tier by ID.
    """
    try:
        logger.info(f"Retrieving subscription tier with ID: {tier_id}")
        tier = get_subscription_tier_by_id(db, str(tier_id))
        return tier
    except Exception as e:
        logger.error(f"Error retrieving subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription tier.")


@router.post("/", response_model=SubscriptionTierOut, dependencies=[Depends(admin_required)])
def create_subscription(
    subscription_data: SubscriptionTierBase,
    db: Session = Depends(get_db),
):
    """
    Create a new subscription tier (Admin only).
    """
    try:
        logger.info(f"Creating subscription tier: {subscription_data.name}")
        tier = create_subscription_tier(db, subscription_data.dict())
        return tier
    except Exception as e:
        logger.error(f"Error creating subscription tier: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create subscription tier.")


@router.put("/{tier_id}", response_model=SubscriptionTierOut, dependencies=[Depends(admin_required)])
def update_subscription(
    tier_id: UUID,
    updated_data: SubscriptionTierBase,
    db: Session = Depends(get_db),
):
    """
    Update an existing subscription tier (Admin only).
    """
    try:
        logger.info(f"Updating subscription tier with ID: {tier_id}")
        tier = update_subscription_tier(db, str(tier_id), updated_data.dict())
        return tier
    except Exception as e:
        logger.error(f"Error updating subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update subscription tier.")


@router.delete("/{tier_id}", dependencies=[Depends(admin_required)])
def delete_subscription(
    tier_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete a subscription tier if no users are subscribed to it (Admin only).
    """
    try:
        logger.info(f"Deleting subscription tier with ID: {tier_id}")
        delete_subscription_tier(db, str(tier_id))
        return {"message": "Subscription tier deleted successfully."}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete subscription tier.")


@router.put("/{tier_id}/deactivate", dependencies=[Depends(admin_required)])
def deactivate_subscription(
    tier_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Deactivate a subscription tier (Admin only).
    """
    try:
        logger.info(f"Deactivating subscription tier with ID: {tier_id}")
        deactivate_subscription_tier(db, str(tier_id))
        return {"message": "Subscription tier deactivated successfully."}
    except Exception as e:
        logger.error(f"Error deactivating subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deactivate subscription tier.")
