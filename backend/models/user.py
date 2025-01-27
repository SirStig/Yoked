from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Table, DateTime, Enum, func, UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.core.database import Base
import uuid
from backend.models.session import SessionModel

# Enum for activity level
from enum import Enum as PyEnum


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

# Association table for friends
user_friends = Table(
    "user_friends",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("friend_id", UUID, ForeignKey("users.id"), primary_key=True),
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

    # New fields
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    activity_level = Column(Enum(ActivityLevel), nullable=True)

    height = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    height_unit = Column(String, default="ft/in")
    weight_unit = Column(String, default="lbs")

    # Versioning for profile changes
    profile_version = Column(Integer, nullable=False, default=1)

    # Privacy fields
    accepted_terms = Column(Boolean, nullable=False)
    accepted_privacy_policy = Column(Boolean, nullable=False)
    accepted_terms_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    accepted_privacy_policy_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # MFA
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String, nullable=True)
    mfa_backup_codes = Column(ARRAY(String), nullable=True)

    # New notification preferences
    email_notifications = Column(Boolean, default=True, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)

    sessions = relationship("SessionModel", back_populates="user", cascade="all, delete-orphan")

    friends = relationship(
        "User",
        secondary=user_friends,
        primaryjoin=id == user_friends.c.user_id,
        secondaryjoin=id == user_friends.c.friend_id,
        backref="friend_of",
    )
    progress_photos = relationship(
        "ProgressPhoto",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

class ProgressPhoto(Base):
    __tablename__ = "progress_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    url = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="progress_photos")
