"""Seed subscription tiers

Revision ID: 201c764921b0
Revises: 617332bb9b1a
Create Date: 2025-02-02 22:03:54.467366
"""

from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import text
import uuid

# revision identifiers, used by Alembic.
revision: str = "201c764921b0"
down_revision: Union[str, None] = "617332bb9b1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Insert subscription tiers
    connection = op.get_bind()

    tiers = [
        {
            "id": str(uuid.uuid4()),
            "name": "Starter",
            "price": 0,
            "currency": "USD",
            "recurring_interval": "monthly",
            "features": [
                'Limited access to "Yoked Reels" with ads.',
                "Basic workout routines with ads.",
                "Read-only access to community forums.",
                "Basic progress tracking tools.",
            ],
            "is_active": True,
            "has_ads": True,
            "access_reels": True,
            "reels_ad_free": False,
            "access_workouts": True,
            "workout_filters": False,
            "access_community_read": True,
            "access_community_post": False,
            "private_community_challenges": False,
            "access_nutrition": False,
            "calorie_tracking": False,
            "personalized_nutrition": False,
            "direct_messaging": False,
            "basic_progress_tracking": True,
            "enhanced_progress_tracking": False,
            "access_live_classes": False,
            "one_on_one_coaching": False,
            "priority_support": False,
            "is_hidden": False,
            "is_trial_available": False,
            "trial_period_days": 0,
            "billing_cycle": "monthly",
            "cancellation_policy": "Cancel anytime",
            "max_reel_uploads": -1,
            "max_saved_workouts": -1,
            "max_messages_per_day": -1,
            "version": 1,
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Champion",
            "price": 999,
            "currency": "USD",
            "recurring_interval": "monthly",
            "features": [
                'Ad-free access to "Yoked Reels" and workout videos.',
                "Expanded workout library with goal-specific filters.",
                "General nutrition articles and healthy recipes.",
                "Full access to community forums with posting privileges.",
                "Direct messaging with other members.",
                "Enhanced progress tracking tools.",
            ],
            "is_active": True,
            "has_ads": False,
            "access_reels": True,
            "reels_ad_free": True,
            "access_workouts": True,
            "workout_filters": True,
            "access_community_read": True,
            "access_community_post": True,
            "private_community_challenges": False,
            "access_nutrition": True,
            "calorie_tracking": False,
            "personalized_nutrition": False,
            "direct_messaging": True,
            "basic_progress_tracking": True,
            "enhanced_progress_tracking": True,
            "access_live_classes": False,
            "one_on_one_coaching": False,
            "priority_support": False,
            "is_hidden": False,
            "is_trial_available": True,
            "trial_period_days": 7,
            "billing_cycle": "monthly",
            "cancellation_policy": "Cancel anytime",
            "max_reel_uploads": -1,
            "max_saved_workouts": -1,
            "max_messages_per_day": -1,
            "version": 1,
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Olympian",
            "price": 1999,
            "currency": "USD",
            "recurring_interval": "monthly",
            "features": [
                "Everything in Champion.",
                "Personalized workout plans tailored to your goals.",
                "Live fitness classes and one-on-one coaching.",
                "Advanced nutrition guidance with calorie tracking tools.",
                "Priority support from the Yoked team.",
                "Exclusive access to private community challenges.",
                "Comprehensive progress analytics and visualizations.",
            ],
            "is_active": True,
            "has_ads": False,
            "access_reels": True,
            "reels_ad_free": True,
            "access_workouts": True,
            "workout_filters": True,
            "access_community_read": True,
            "access_community_post": True,
            "private_community_challenges": True,
            "access_nutrition": True,
            "calorie_tracking": True,
            "personalized_nutrition": True,
            "direct_messaging": True,
            "basic_progress_tracking": True,
            "enhanced_progress_tracking": True,
            "access_live_classes": True,
            "one_on_one_coaching": True,
            "priority_support": True,
            "is_hidden": False,
            "is_trial_available": True,
            "trial_period_days": 3,
            "billing_cycle": "monthly",
            "cancellation_policy": "Cancel anytime",
            "max_reel_uploads": -1,
            "max_saved_workouts": -1,
            "max_messages_per_day": -1,
            "version": 1,
        },
    ]

    for tier in tiers:
        connection.execute(
            text(
                """
                INSERT INTO subscription_tiers (
                    id, name, price, currency, recurring_interval, features, is_active, has_ads, 
                    access_reels, reels_ad_free, access_workouts, workout_filters, 
                    access_community_read, access_community_post, private_community_challenges, 
                    access_nutrition, calorie_tracking, personalized_nutrition, direct_messaging, 
                    basic_progress_tracking, enhanced_progress_tracking, access_live_classes, 
                    one_on_one_coaching, priority_support, is_hidden, is_trial_available, trial_period_days, 
                    billing_cycle, cancellation_policy, max_reel_uploads, max_saved_workouts, 
                    max_messages_per_day, version, created_at, updated_at
                ) VALUES (
                    :id, :name, :price, :currency, :recurring_interval, :features, :is_active, :has_ads, 
                    :access_reels, :reels_ad_free, :access_workouts, :workout_filters, 
                    :access_community_read, :access_community_post, :private_community_challenges, 
                    :access_nutrition, :calorie_tracking, :personalized_nutrition, :direct_messaging, 
                    :basic_progress_tracking, :enhanced_progress_tracking, :access_live_classes, 
                    :one_on_one_coaching, :priority_support, :is_hidden, :is_trial_available, :trial_period_days, 
                    :billing_cycle, :cancellation_policy, :max_reel_uploads, :max_saved_workouts, 
                    :max_messages_per_day, :version, NOW(), NOW()
                )
                """
            ),
            tier,
        )


def downgrade():
    connection = op.get_bind()
    connection.execute(text("DELETE FROM subscription_tiers WHERE name IN ('Starter', 'Champion', 'Olympian');"))
