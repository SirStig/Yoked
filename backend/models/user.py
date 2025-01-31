from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Table, DateTime, Enum, func, UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base
import uuid
from enum import Enum as PyEnum

from backend.models.community_post import post_likes, post_bookmarks
from backend.models.private_messaging import group_chat_participants
from backend.models.reels import reel_likes, reel_bookmarks
from backend.models.workout import workout_bookmarks
from backend.models.nutrition import saved_meal_plans


class ActivityLevel(PyEnum):
    sedentary = "Sedentary"
    lightly_active = "Lightly Active"
    active = "Active"
    very_active = "Very Active"

class SetupStep(PyEnum):
    email_verification = "verify_email"
    profile_completion = "profile_completion"
    subscription_selection = "subscription_selection"
    completed = "completed"

class UserType(PyEnum):
    REGULAR = "regular"
    ADMIN = "admin"

# Association table for followers
user_followers = Table(
    "user_followers",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("follower_id", UUID, ForeignKey("users.id"), primary_key=True),
)

# Association table for friend requests
friend_requests = Table(
    "friend_requests",
    Base.metadata,
    Column("sender_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("receiver_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("status", String, default="pending", nullable=False),
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String, nullable=True)
    fitness_goals = Column(String, nullable=True)
    subscription_plan = Column(String, default="Free")
    setup_step = Column(Enum(SetupStep), default=SetupStep.email_verification)
    joined_at = Column(DateTime, default=datetime.utcnow)
    user_type = Column(Enum(UserType), default=UserType.REGULAR, nullable=False)
    admin_secret_key = Column(String, nullable=True)
    flagged_for_review = Column(Boolean, default=False)

    # Additional Fields
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    activity_level = Column(Enum(ActivityLevel), nullable=True)
    height = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    height_unit = Column(String, default="ft/in")
    weight_unit = Column(String, default="lbs")

    # Versioning
    profile_version = Column(Integer, nullable=False, default=1)

    # Privacy settings
    accepted_terms = Column(Boolean, nullable=False)
    accepted_privacy_policy = Column(Boolean, nullable=False)
    accepted_terms_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    accepted_privacy_policy_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # MFA
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String, nullable=True)
    mfa_backup_codes = Column(ARRAY(String), nullable=True)

    # Notification Preferences
    email_notifications = Column(Boolean, default=True, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)

    # Relationships
    sessions = relationship("SessionModel", back_populates="user", cascade="all, delete-orphan")
    followers = relationship("User", secondary=user_followers, primaryjoin=id == user_followers.c.user_id, secondaryjoin=id == user_followers.c.follower_id, backref="following")
    friend_requests_sent = relationship("User", secondary=friend_requests, primaryjoin=id == friend_requests.c.sender_id, secondaryjoin=id == friend_requests.c.receiver_id, backref="friend_requests_received")
    progress_photos = relationship("ProgressPhoto", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship(
        "UserSubscription",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    liked_posts = relationship("Post", secondary=post_likes, back_populates="likes")
    bookmarked_posts = relationship("Post", secondary=post_bookmarks, back_populates="bookmarks")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    reported_posts = relationship("ReportedPost", back_populates="reporter", cascade="all, delete-orphan")
    reels = relationship("Reel", back_populates="author", cascade="all, delete-orphan")
    liked_reels = relationship("Reel", secondary=reel_likes, back_populates="likes")
    bookmarked_reels = relationship("Reel", secondary=reel_bookmarks, back_populates="bookmarks")
    reel_comments = relationship("ReelComment", back_populates="author", cascade="all, delete-orphan")
    reported_reels = relationship("ReportedReel", back_populates="reporter", cascade="all, delete-orphan")
    bookmarked_workouts = relationship("Workout", secondary=workout_bookmarks, back_populates="bookmarks")
    workout_history = relationship("WorkoutProgress", back_populates="user", cascade="all, delete-orphan")
    nutrition_articles = relationship("NutritionArticle", back_populates="author", cascade="all, delete-orphan")
    saved_meal_plans = relationship("MealPlan", secondary=saved_meal_plans, back_populates="users_saved")
    meal_tracking = relationship("UserMealTracking", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", secondary=group_chat_participants, back_populates="participants")
    messages_sent = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    typing_status = relationship("TypingStatus", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    level = relationship("UserLevel", back_populates="user", cascade="all, delete-orphan")
    leaderboard = relationship("Leaderboard", back_populates="user", cascade="all, delete-orphan")


class ProgressPhoto(Base):
    __tablename__ = "progress_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="progress_photos")
