from sqlalchemy.orm import Session
from backend.models.subscription_tier import SubscriptionTier
from backend.core.database import engine, Base
from datetime import datetime

# Define subscription tier data
subscription_tiers = [
    {
        "name": "Starter",
        "price": 0,
        "features": [
            "Limited access to 'Yoked Reels' with ads.",
            "Basic workout routines with ads.",
            "Read-only access to community forums.",
            "Basic progress tracking tools."
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
        "highlight": "Free forever",
    },
    {
        "name": "Champion",
        "price": 999,
        "features": [
            "Ad-free access to 'Yoked Reels' and workout videos.",
            "Expanded workout library with goal-specific filters.",
            "General nutrition articles and healthy recipes.",
            "Full access to community forums with posting privileges.",
            "Direct messaging with other members.",
            "Enhanced progress tracking tools."
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
        "highlight": "Most popular plan",
    },
    {
        "name": "Olympian",
        "price": 1999,
        "features": [
            "Everything in Champion.",
            "Personalized workout plans tailored to your goals.",
            "Live fitness classes and one-on-one coaching.",
            "Advanced nutrition guidance with calorie tracking tools.",
            "Priority support from the Yoked team.",
            "Exclusive access to private community challenges.",
            "Comprehensive progress analytics and visualizations."
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
        "highlight": "Premium access for serious fitness enthusiasts",
    },
]


def seed_subscription_tiers(db: Session):
    """
    Seed the database with predefined subscription tiers.
    """
    for tier in subscription_tiers:
        existing_tier = db.query(SubscriptionTier).filter_by(name=tier["name"]).first()
        if not existing_tier:
            new_tier = SubscriptionTier(**tier)
            db.add(new_tier)
    db.commit()


if __name__ == "__main__":
    # Initialize database session
    Base.metadata.create_all(bind=engine)
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        seed_subscription_tiers(db)
        print("Subscription tiers seeded successfully.")
    except Exception as e:
        print(f"Error seeding subscription tiers: {e}")
    finally:
        db.close()
