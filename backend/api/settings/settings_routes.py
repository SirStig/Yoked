import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user
from backend.models import Payment, SubscriptionTier
from backend.models.user import User
from backend.schemas.user_schema import (
    NotificationPreferences,
    UserProfileUpdate,
    PrivacySettings,
    SecuritySettings,
    ThemePreferences,
    ThirdPartyAccounts
)
from backend.services.mfa import reset_mfa
from backend.core.logging_config import get_logger
from backend.schemas.payment_schema import SubscriptionDetails, UpdateSubscription, RefundRequest
from backend.services.session_service import fetch_user_sessions
from backend.api.subscriptions.subscription_service import update_user_subscription, cancel_user_subscription
from backend.schemas.session_schema import UserSession

# Initialize Stripe API
stripe.api_key = "your-stripe-secret-key"

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter(prefix="/api/settings", tags=["Settings"])

### **Notification Settings**
@router.get("/notifications", response_model=NotificationPreferences)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """ Fetch the current user's notification preferences. """
    return {
        "email_notifications": current_user.email_notifications,
        "push_notifications": current_user.push_notifications,
    }

@router.put("/notifications", response_model=dict)
async def update_notification_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update the user's notification preferences. """
    current_user.email_notifications = preferences.email_notifications
    current_user.push_notifications = preferences.push_notifications
    db.commit()
    return {"message": "Notification preferences updated successfully."}

### **Profile Settings**
@router.put("/profile", response_model=dict)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update the user's profile information. """
    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    return {"message": "Profile updated successfully."}

### **Privacy Settings**
@router.put("/privacy", response_model=dict)
async def update_privacy_settings(
    privacy_data: PrivacySettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update the user's privacy settings. """
    for key, value in privacy_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    return {"message": "Privacy settings updated successfully."}

### **Security Settings**
@router.put("/security", response_model=dict)
async def update_security_settings(
    security_data: SecuritySettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update the user's security settings. """
    for key, value in security_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    return {"message": "Security settings updated successfully."}

### **Theme & UI Preferences**
@router.put("/theme", response_model=dict)
async def update_theme_settings(
    theme_data: ThemePreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update theme settings for dark mode, font size, etc. """
    for key, value in theme_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    return {"message": "Theme settings updated successfully."}

### **Third-Party Account Connections**
@router.put("/third-party", response_model=dict)
async def update_third_party_accounts(
    account_data: ThirdPartyAccounts,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update the user's connected third-party accounts. """
    for key, value in account_data.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    return {"message": "Third-party accounts updated successfully."}

### **Subscription Management**
@router.put("/subscription", response_model=dict)
async def update_subscription(
    subscription_data: UpdateSubscription,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update a user's subscription via Stripe. """
    current_subscription = stripe.Subscription.retrieve(current_user.stripe_subscription_id)
    new_plan_id = subscription_data.new_plan_id

    # Fetch new plan
    new_plan = db.query(SubscriptionTier).filter_by(id=new_plan_id, is_active=True).first()
    if not new_plan:
        raise HTTPException(status_code=400, detail="Invalid subscription plan.")

    stripe.Subscription.modify(
        current_subscription["id"],
        cancel_at_period_end=False,
        proration_behavior="create_prorations",
        items=[{"id": current_subscription["items"]["data"][0]["id"], "price": new_plan.stripe_price_id}],
    )

    current_user.subscription_plan = new_plan.name
    current_user.subscription_price = new_plan.price
    db.commit()
    return {"message": "Subscription updated successfully."}

### **Refund Management**
@router.post("/refund", response_model=dict)
async def request_refund(
    refund_request: RefundRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Process a refund via Stripe. """
    payment = db.query(Payment).filter(Payment.id == refund_request.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found.")

    stripe.Refund.create(payment_intent=payment.stripe_payment_id)
    payment.status = "REFUNDED"
    db.commit()
    return {"message": "Refund processed successfully."}
