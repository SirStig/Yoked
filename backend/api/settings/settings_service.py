from sqlalchemy.orm import Session

from backend.models.subscription_tier import UserSubscription, SubscriptionTier
from backend.models.user import User
from backend.models.session import SessionModel
from backend.schemas.user_schema import (
    UserProfileUpdate, PasswordChange, PrivacySettings, EmailUpdateRequest
)
from backend.api.auth.auth_service import hash_password, verify_password
from backend.core.logging_config import get_logger
from fastapi import HTTPException
from datetime import datetime, timedelta
from backend.models.payment import PaymentPlatform
from backend.api.payments.payment_service import cancel_subscription_stripe, update_subscription_stripe
from backend.schemas.subscription_tier_schema import UpdateSubscription
from backend.schemas.notifications_schema import NotificationPreferences
from backend.services.email_service import send_verification_email

logger = get_logger(__name__)

class SettingsService:

    @staticmethod
    def update_profile(db: Session, user: User, profile_data: UserProfileUpdate):
        """
        Update user profile details (name, bio, fitness goals, etc.).
        """
        if profile_data.full_name:
            user.full_name = profile_data.full_name
        if profile_data.bio:
            user.bio = profile_data.bio
        if profile_data.height:
            user.height = profile_data.height
        if profile_data.weight:
            user.weight = profile_data.weight
        if profile_data.fitness_goals:
            user.fitness_goals = profile_data.fitness_goals

        db.commit()
        return {"message": "Profile updated successfully."}

    @staticmethod
    def update_email(db: Session, user: User, email_data: EmailUpdateRequest):
        """
        Update user email (requires verification).
        """
        existing_user = db.query(User).filter(User.email == email_data.new_email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already in use.")

        verification_code = send_verification_email(email_data.new_email)
        user.pending_email = email_data.new_email
        user.email_verification_code = verification_code
        db.commit()

        return {"message": "Email update initiated. Please verify your new email."}

    @staticmethod
    def verify_email_change(db: Session, user: User, verification_code: str):
        """
        Verify new email using a code sent to the user's email.
        """
        if user.email_verification_code != verification_code:
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        user.email = user.pending_email
        user.pending_email = None
        user.email_verification_code = None
        db.commit()

        return {"message": "Email updated successfully."}

    @staticmethod
    def change_password(db: Session, user: User, password_data: PasswordChange):
        """
        Change user password (requires OTP or current password verification).
        """
        if not verify_password(password_data.current_password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Current password is incorrect.")

        user.hashed_password = hash_password(password_data.new_password)
        db.commit()

        return {"message": "Password updated successfully."}

    @staticmethod
    def toggle_mfa(db: Session, user: User, enable_mfa: bool):
        """
        Enable or disable MFA for user security.
        """
        user.mfa_enabled = enable_mfa
        db.commit()
        return {"message": "MFA setting updated."}

    @staticmethod
    def fetch_sessions(db: Session, user: User):
        """
        Fetch all active sessions for the user.
        """
        return db.query(SessionModel).filter_by(user_id=user.id).all()

    @staticmethod
    def revoke_session(db: Session, user: User, session_id: str):
        """
        Revoke (logout) a specific session.
        """
        session = db.query(SessionModel).filter_by(id=session_id, user_id=user.id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found.")

        db.delete(session)
        db.commit()
        return {"message": "Session revoked successfully."}

    @staticmethod
    def get_subscription(db: Session, user: User):
        """
        Fetch user's current subscription details, ensuring all necessary fields are returned.
        """
        subscription = db.query(UserSubscription).filter_by(user_id=user.id).first()

        if not subscription:
            raise HTTPException(status_code=404, detail="No active subscription found.")

        # Fetch the associated subscription tier
        tier = db.query(SubscriptionTier).filter_by(id=subscription.subscription_tier_id).first()

        if not tier:
            raise HTTPException(status_code=500, detail="Subscription tier data is missing.")

        return {
            "subscription_name": tier.name,
            "price": tier.price,
            "currency": tier.currency,
            "renewal_date": subscription.end_date,
            "status": subscription.status,
        }

    @staticmethod
    def update_subscription(db: Session, user: User, subscription_data: UpdateSubscription):
        """
        Update the user's subscription via Stripe.
        """
        subscription = db.query(UserSubscription).filter_by(user_id=user.id).first()
        if not subscription:
            raise HTTPException(status_code=404, detail="No active subscription found.")

        # Handle only Stripe subscriptions for now
        if subscription.platform == PaymentPlatform.STRIPE:
            return update_subscription_stripe(user, subscription, subscription_data)

        raise HTTPException(status_code=400, detail="Only Stripe subscriptions are supported currently.")

    @staticmethod
    def cancel_subscription(db: Session, user: User, password: str):
        """
        Cancel the user's subscription via Stripe (requires password verification).
        """
        subscription = db.query(UserSubscription).filter_by(user_id=user.id).first()
        if not subscription:
            raise HTTPException(status_code=404, detail="No active subscription found.")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password.")

        # Handle only Stripe subscription cancellations
        if subscription.platform == PaymentPlatform.STRIPE:
            return cancel_subscription_stripe(user, subscription)

        raise HTTPException(status_code=400, detail="Only Stripe subscriptions are supported currently.")

    @staticmethod
    def get_notifications(db: Session, user: User):
        """
        Fetch the current user's notification preferences.
        """
        return {
            "likes": user.notifications_likes,
            "comments": user.notifications_comments,
            "follows": user.notifications_follows,
            "direct_messages": user.notifications_messages,
            "subscriptions": user.notifications_subscriptions,
            "marketing": user.notifications_marketing
        }

    @staticmethod
    def update_notifications(db: Session, user: User, preferences: NotificationPreferences):
        """
        Update notification preferences.
        """
        user.notifications_likes = preferences.likes
        user.notifications_comments = preferences.comments
        user.notifications_follows = preferences.follows
        user.notifications_messages = preferences.direct_messages
        user.notifications_subscriptions = preferences.subscriptions
        user.notifications_marketing = preferences.marketing

        db.commit()
        return {"message": "Notification preferences updated successfully."}

    @staticmethod
    def update_privacy(db: Session, user: User, privacy_settings: PrivacySettings):
        """
        Update privacy settings for the user.
        """
        user.profile_visibility = privacy_settings.profile_visibility
        user.reels_visibility = privacy_settings.reels_visibility
        user.comments_visibility = privacy_settings.comments_visibility

        db.commit()
        return {"message": "Privacy settings updated successfully."}

    @staticmethod
    def initiate_email_verification(db: Session, user: User, new_email: str):
        """
        Sends a verification email to the new email address.
        """
        existing_user = db.query(User).filter(User.email == new_email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use.")

        verification_code = send_verification_email(new_email)
        user.pending_email = new_email
        user.email_verification_code = verification_code
        db.commit()

        return {"message": "Verification code sent to new email."}

    @staticmethod
    def verify_email_update(db: Session, user: User, verification_code: str):
        """
        Verify email using the code sent to the new email.
        """
        if user.email_verification_code != verification_code:
            raise HTTPException(status_code=400, detail="Invalid verification code.")

        user.email = user.pending_email
        user.pending_email = None
        user.email_verification_code = None
        db.commit()

        return {"message": "Email updated successfully."}

    @staticmethod
    def delete_account(db: Session, user: User, password: str):
        """
        Deletes the user's account (requires password verification).
        Cancels subscriptions first.
        """
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password.")

        subscription = db.query(UserSubscription).filter_by(user_id=user.id).first()
        if subscription:
            # Cancel subscription before deleting the account
            if subscription.platform == PaymentPlatform.STRIPE:
                cancel_subscription_stripe(user, subscription)

        db.delete(user)
        db.commit()

        return {"message": "Account deleted successfully."}
