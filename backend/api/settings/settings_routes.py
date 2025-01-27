from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user
from backend.models.user import User
from backend.schemas.user_schema import NotificationPreferences, UserProfileUpdate
from backend.services.mfa import reset_mfa
from backend.core.logging_config import get_logger
from backend.schemas.payment_schema import SubscriptionDetails, UpdateSubscription
from backend.services.session_service import fetch_user_sessions
from backend.api.subscriptions.subscription_service import update_user_subscription, cancel_user_subscription
from backend.schemas.session_schema import UserSession

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter(prefix="/api/settings", tags=["Settings"])


@router.get("/notifications", response_model=NotificationPreferences)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's notification preferences.
    """
    logger.info(f"Fetching notification preferences for user ID {current_user.id}")
    try:
        return {
            "email_notifications": current_user.email_notifications,
            "push_notifications": current_user.push_notifications,
        }
    except Exception as e:
        logger.exception(f"Error fetching notification preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch notification preferences.")


@router.put("/notifications", response_model=dict)
async def update_notification_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's notification preferences.
    """
    logger.info(f"Updating notification preferences for user ID {current_user.id}")
    try:
        current_user.email_notifications = preferences.email_notifications
        current_user.push_notifications = preferences.push_notifications
        db.commit()

        logger.info(f"Notification preferences updated for user ID {current_user.id}")
        return {"message": "Notification preferences updated successfully."}
    except Exception as e:
        logger.exception(f"Error updating notification preferences: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update notification preferences.")


@router.put("/reset-mfa", response_model=dict)
async def reset_mfa_route(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Reset the user's MFA setup.
    """
    logger.info(f"Resetting MFA for user ID {current_user.id}")
    try:
        reset_mfa(current_user.id, db)
        logger.info(f"MFA reset successfully for user ID {current_user.id}")
        return {"message": "MFA reset successfully. Please set up MFA again."}
    except Exception as e:
        logger.exception(f"Error resetting MFA: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to reset MFA.")


@router.delete("/account", response_model=dict)
async def delete_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Delete the user's account.
    """
    logger.info(f"Deleting account for user ID {current_user.id}")
    try:
        db.delete(current_user)
        db.commit()

        logger.info(f"Account deleted for user ID {current_user.id}")
        return {"message": "Account deleted successfully."}
    except Exception as e:
        logger.exception(f"Error deleting account: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete account.")


@router.get("/subscription", response_model=SubscriptionDetails)
async def get_subscription_details(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's subscription details.
    """
    logger.info(f"Fetching subscription details for user ID {current_user.id}")
    try:
        return {
            "subscription_name": current_user.subscription_plan,
            "price": current_user.subscription_price,
            "status": current_user.subscription_status,
        }
    except Exception as e:
        logger.exception(f"Error fetching subscription details: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscription details.")


@router.put("/subscription", response_model=dict)
async def update_subscription(
    subscription_data: UpdateSubscription,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's subscription plan.
    """
    logger.info(f"Updating subscription for user ID {current_user.id}")
    try:
        update_user_subscription(current_user.id, subscription_data, db)
        logger.info(f"Subscription updated successfully for user ID {current_user.id}")
        return {"message": "Subscription updated successfully."}
    except Exception as e:
        logger.exception(f"Error updating subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update subscription.")


@router.delete("/subscription", response_model=dict)
async def cancel_subscription(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Cancel the user's subscription plan.
    """
    logger.info(f"Cancelling subscription for user ID {current_user.id}")
    try:
        cancel_user_subscription(current_user.id, db)
        logger.info(f"Subscription cancelled successfully for user ID {current_user.id}")
        return {"message": "Subscription cancelled successfully."}
    except Exception as e:
        logger.exception(f"Error cancelling subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel subscription.")


@router.get("/sessions", response_model=list[UserSession])
async def get_user_sessions(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's active sessions.
    """
    logger.info(f"Fetching sessions for user ID {current_user.id}")
    try:
        sessions = fetch_user_sessions(current_user.id, db)
        return sessions
    except Exception as e:
        logger.exception(f"Error fetching sessions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch sessions.")
