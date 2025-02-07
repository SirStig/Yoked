from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from sqlalchemy.orm import relationship

from backend.core.database import Base

class SubscriptionTier(Base):
    __tablename__ = "subscription_tiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    features = Column(ARRAY(String), nullable=True)
    is_active = Column(Boolean, default=False)
    currency = Column(String, nullable=False, default="USD")
    recurring_interval = Column(String, nullable=False, default="monthly")  # Can be "monthly" or "yearly"

    # Capability flags
    has_ads = Column(Boolean, default=True)
    access_reels = Column(Boolean, default=False)
    reels_ad_free = Column(Boolean, default=False)

    access_workouts = Column(Boolean, default=False)
    workout_filters = Column(Boolean, default=False)

    access_community_read = Column(Boolean, default=False)
    access_community_post = Column(Boolean, default=False)
    private_community_challenges = Column(Boolean, default=False)

    access_nutrition = Column(Boolean, default=False)
    calorie_tracking = Column(Boolean, default=False)
    personalized_nutrition = Column(Boolean, default=False)

    direct_messaging = Column(Boolean, default=False)

    basic_progress_tracking = Column(Boolean, default=False)
    enhanced_progress_tracking = Column(Boolean, default=False)

    access_live_classes = Column(Boolean, default=False)
    one_on_one_coaching = Column(Boolean, default=False)

    priority_support = Column(Boolean, default=False)

    # Hide tier from new users but keep it for existing subscribers
    is_hidden = Column(Boolean, default=False)

    # Free trial settings
    is_trial_available = Column(Boolean, default=False)
    trial_period_days = Column(Integer, default=0)

    # Billing and cancellation policies
    billing_cycle = Column(String, default="monthly")  # Can be "monthly" or "yearly"
    cancellation_policy = Column(String, default="Cancel anytime")

    # Usage Restrictions
    max_reel_uploads = Column(Integer, default=0)
    max_saved_workouts = Column(Integer, default=0)
    max_messages_per_day = Column(Integer, default=0)

    # Versioning
    version = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Linking subscriptions to users
class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    subscription_tier_id = Column(UUID(as_uuid=True), ForeignKey("subscription_tiers.id"), nullable=False)
    status = Column(String, default="active")  # Can be "active", "canceled", "expired"
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)
    renewal_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")
