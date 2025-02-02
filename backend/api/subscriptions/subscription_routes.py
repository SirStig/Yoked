from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from uuid import UUID
import stripe

from backend.core.database import get_db
from backend.api.auth.auth_service import admin_required, get_current_user
from backend.models import User
from backend.schemas.payment_schema import SubscriptionDetails, UpdateSubscription, RefundRequest
from backend.api.subscriptions.subscription_service import (
    get_all_subscription_tiers,
    get_subscription_tier_by_id,
    create_subscription_tier,
    update_subscription_tier,
    deactivate_subscription_tier,
    delete_subscription_tier,
    update_user_subscription,
    cancel_user_subscription,
    process_refund
)
from backend.models.subscription_tier import SubscriptionTier
from backend.core.config import settings
from backend.core.logging_config import get_logger

logger = get_logger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/api/subscriptions", tags=["Subscriptions"])

### **List Subscription Tiers**
@router.get("/", response_model=List[SubscriptionDetails])
def list_subscription_tiers(
    include_inactive: bool = Query(False, description="Include inactive subscription tiers"),
    db: Session = Depends(get_db),
):
    """ List all subscription tiers, including inactive ones if requested. """
    try:
        logger.info("Fetching all subscription tiers.")
        return get_all_subscription_tiers(db, include_inactive)
    except Exception as e:
        logger.error(f"Error listing subscription tiers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list subscription tiers.")

### **Retrieve a Specific Subscription Tier**
@router.get("/{tier_id}", response_model=SubscriptionDetails)
def retrieve_subscription_tier(
    tier_id: UUID,
    db: Session = Depends(get_db),
):
    """ Retrieve a specific subscription tier by ID. """
    try:
        logger.info(f"Fetching subscription tier: {tier_id}")
        return get_subscription_tier_by_id(db, str(tier_id))
    except Exception as e:
        logger.error(f"Error retrieving subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve subscription tier.")

### **Create Subscription Tier (Admin Only)**
@router.post("/", response_model=SubscriptionDetails, dependencies=[Depends(admin_required)])
def create_subscription(
    subscription_data: SubscriptionDetails,
    db: Session = Depends(get_db),
):
    """ Create a new subscription tier (Admin only). """
    try:
        logger.info(f"Creating subscription tier: {subscription_data.plan_name}")
        tier = create_subscription_tier(db, subscription_data.dict())

        tier.version += 1
        db.commit()

        logger.info(f"Subscription tier created: {tier.plan_name}")
        return tier
    except Exception as e:
        logger.error(f"Error creating subscription tier: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create subscription tier.")

### **Update Subscription Tier (Admin Only)**
@router.put("/{tier_id}", response_model=SubscriptionDetails, dependencies=[Depends(admin_required)])
def update_subscription(
    tier_id: UUID,
    updated_data: SubscriptionDetails,
    db: Session = Depends(get_db),
):
    """ Update an existing subscription tier (Admin only). """
    try:
        logger.info(f"Updating subscription tier: {tier_id}")
        tier = update_subscription_tier(db, str(tier_id), updated_data.dict())

        tier.version += 1
        db.commit()

        return tier
    except Exception as e:
        logger.error(f"Error updating subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update subscription tier.")

### **Deactivate Subscription Tier (Admin Only)**
@router.put("/{tier_id}/deactivate", dependencies=[Depends(admin_required)])
def deactivate_subscription(
    tier_id: UUID,
    db: Session = Depends(get_db),
):
    """ Deactivate a subscription tier (Admin only). """
    try:
        logger.info(f"Deactivating subscription tier: {tier_id}")
        deactivate_subscription_tier(db, str(tier_id))

        db.commit()
        return {"message": "Subscription tier deactivated successfully."}
    except Exception as e:
        logger.error(f"Error deactivating subscription tier {tier_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deactivate subscription tier.")

### **Cancel Subscription (User)**
@router.delete("/cancel", response_model=dict)
def cancel_user_subscription_route(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Cancel a user's subscription via Stripe. """
    try:
        cancel_user_subscription(current_user.id, db)
        return {"message": "Subscription cancelled successfully."}
    except Exception as e:
        logger.error(f"Error cancelling subscription for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription.")

### **Process Refund (User)**
@router.post("/refund", response_model=dict)
def request_refund(
    refund_request: RefundRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Process a refund request via Stripe. """
    try:
        process_refund(refund_request, current_user.id, db)
        return {"message": "Refund request processed successfully."}
    except Exception as e:
        logger.error(f"Error processing refund for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process refund.")
