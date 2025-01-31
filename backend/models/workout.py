from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, Boolean, Table, ForeignKey, UUID, ARRAY, func
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime
from enum import Enum as PyEnum

from backend.models.tags import workout_tags

# Association table for workout bookmarks
workout_bookmarks = Table(
    "workout_bookmarks",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("workout_id", UUID, ForeignKey("workouts.id"), primary_key=True),
)

class DifficultyLevel(PyEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Categorization & Muscle Groups
    category = Column(String, nullable=False)  # e.g., Strength, Cardio, Yoga
    subcategory = Column(String, nullable=True)  # e.g., HIIT, Bodybuilding
    muscle_groups = Column(ARRAY(String), nullable=True)  # e.g., ["Chest", "Legs"]

    # Equipment & Difficulty
    equipment = Column(ARRAY(String), nullable=True)  # e.g., ["Dumbbells", "Resistance Bands"]
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in minutes

    # Video storage (Vimeo)
    video_vimeo_url = Column(String, nullable=False)  # Vimeo Link

    # Engagement Metrics
    times_completed = Column(Integer, default=0)  # How many users completed this
    likes_count = Column(Integer, default=0)
    bookmarks_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)

    # Tags & Filtering
    tags = relationship("Tag", secondary=workout_tags, back_populates="workouts")

    # Relationships
    bookmarks = relationship("User", secondary=workout_bookmarks, back_populates="bookmarked_workouts")

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkoutProgress(Base):
    __tablename__ = "workout_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workout_id = Column(UUID(as_uuid=True), ForeignKey("workouts.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    workout = relationship("Workout")
    user = relationship("User", back_populates="workout_history")

