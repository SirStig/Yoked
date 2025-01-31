from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID, func
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "10 Workouts Completed"
    description = Column(String, nullable=False)  # e.g., "Completed 10 workouts in a month"
    icon_url = Column(String, nullable=True)  # Optional badge image URL

    created_at = Column(DateTime, default=datetime.utcnow)


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    achievement_id = Column(UUID(as_uuid=True), ForeignKey("achievements.id"), nullable=False)

    earned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")


class UserLevel(Base):
    __tablename__ = "user_levels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    level = Column(Integer, default=1)  # User's level
    experience_points = Column(Integer, default=0)  # XP earned
    next_level_xp = Column(Integer, default=100)  # XP required for next level

    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="level")


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    total_points = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)  # Global ranking

    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="leaderboard")
