from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.sql import func
from backend.core.database import Base
from enum import Enum as PyEnum

class DifficultyLevel(PyEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    equipment = Column(Text, nullable=True)
    video_url = Column(String, nullable=False)  # Vimeo link
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
