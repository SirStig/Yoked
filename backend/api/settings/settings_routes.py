from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user
from backend.api.settings.settings_service import SettingsService
from backend.models.user import User
from backend.schemas.user_schema import (
    UserProfileUpdate, SecuritySettings, PasswordChange, PrivacySettings, EmailUpdateRequest
)
from backend.schemas.subscription_tier_schema import SubscriptionDetails, UpdateSubscription
from backend.schemas.session_schema import UserSession
from backend.schemas.notifications_schema import NotificationPreferences
from backend.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()

### **Profile Management**
@router.put("/profile", response_model=dict)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user profile details (name, bio, height, weight, fitness goals, etc.).
    """
    return SettingsService.update_profile(db, current_user, profile_data)

@router.put("/email", response_model=dict)
async def update_email(
    email_data: EmailUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update user email (requires email verification).
    """
    return SettingsService.update_email(db, current_user, email_data)

### **Security & Authentication**
@router.put("/password", response_model=dict)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Change user password (requires OTP or current password verification).
    """
    return SettingsService.change_password(db, current_user, password_data)

@router.put("/mfa", response_model=dict)
async def toggle_mfa(
    enable_mfa: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Enable or disable MFA for user security.
    """
    return SettingsService.toggle_mfa(db, current_user, enable_mfa)

@router.get("/sessions", response_model=list[UserSession])
async def get_user_sessions(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's active sessions.
    """
    return SettingsService.fetch_sessions(db, current_user)

@router.delete("/sessions/{session_id}", response_model=dict)
async def revoke_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Revoke a specific session (logout from a device).
    """
    return SettingsService.revoke_session(db, current_user, session_id)

### **Subscription Management**
@router.get("/subscription", response_model=SubscriptionDetails)
async def get_subscription_details(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the user's current subscription details.
    """
    return SettingsService.get_subscription(db, current_user)

@router.put("/subscription", response_model=dict)
async def update_subscription(
    subscription_data: UpdateSubscription,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's subscription plan (Stripe, Apple, or Google).
    """
    return SettingsService.update_subscription(db, current_user, subscription_data)

@router.delete("/subscription", response_model=dict)
async def cancel_subscription(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Cancel the user's subscription (Stripe, Apple, Google).
    Requires password verification.
    """
    return SettingsService.cancel_subscription(db, current_user)

### **Notification Preferences**
@router.get("/notifications", response_model=NotificationPreferences)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's notification preferences.
    """
    return SettingsService.get_notifications(db, current_user)

@router.put("/notifications", response_model=dict)
async def update_notification_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the user's notification preferences (email & push notifications for likes, comments, follows, etc.).
    """
    return SettingsService.update_notifications(db, current_user, preferences)

### **Privacy Settings**
@router.put("/privacy", response_model=dict)
async def update_privacy_settings(
    privacy_settings: PrivacySettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update privacy settings for the user (who can see profile, reels, posts).
    """
    return SettingsService.update_privacy(db, current_user, privacy_settings)

### **Reels & Community Post Settings**
@router.put("/reels", response_model=dict)
async def update_reels_settings(
    reels_settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update reels settings (privacy, auto-moderation).
    """
    return SettingsService.update_reels_settings(db, current_user, reels_settings)

@router.put("/community", response_model=dict)
async def update_community_settings(
    community_settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update community post settings (visibility, flagged content settings).
    """
    return SettingsService.update_community_settings(db, current_user, community_settings)

### **Nutrition & Workout Preferences**
@router.put("/nutrition", response_model=dict)
async def update_nutrition_settings(
    nutrition_settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update nutrition settings (dietary preferences, calorie tracking).
    """
    return SettingsService.update_nutrition_settings(db, current_user, nutrition_settings)

@router.put("/workout", response_model=dict)
async def update_workout_settings(
    workout_settings: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update workout settings (activity level, progress tracking).
    """
    return SettingsService.update_workout_settings(db, current_user, workout_settings)

### **Account Deletion**
@router.delete("/account", response_model=dict)
async def delete_account(
    password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete the user's account permanently (requires password verification & subscription cancellation).
    """
    return SettingsService.delete_account(db, current_user, password)
