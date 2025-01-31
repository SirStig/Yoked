from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, UUID, ARRAY, func
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime

# Association table for user-saved meal plans
saved_meal_plans = Table(
    "saved_meal_plans",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("meal_plan_id", UUID, ForeignKey("meal_plans.id"), primary_key=True),
)


class NutritionArticle(Base):
    __tablename__ = "nutrition_articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    category = Column(String, nullable=False)  # e.g., "Weight Loss", "Muscle Gain"
    tags = Column(ARRAY(String), nullable=True)  # Tags for searchability

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="nutrition_articles")


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # Diet filters
    diet_type = Column(String, nullable=False)  # e.g., "Keto", "Vegan", "High-Protein"

    # Macros & Calories
    total_calories = Column(Integer, nullable=False)
    protein_grams = Column(Integer, nullable=True)
    carb_grams = Column(Integer, nullable=True)
    fat_grams = Column(Integer, nullable=True)

    # Relationships
    users_saved = relationship("User", secondary=saved_meal_plans, back_populates="saved_meal_plans")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserMealTracking(Base):
    __tablename__ = "user_meal_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    meal_plan_id = Column(UUID(as_uuid=True), ForeignKey("meal_plans.id"), nullable=True)

    date_tracked = Column(DateTime, default=datetime.utcnow, nullable=False)
    calories_consumed = Column(Integer, nullable=False)
    protein_grams = Column(Integer, nullable=True)
    carb_grams = Column(Integer, nullable=True)
    fat_grams = Column(Integer, nullable=True)

    meal_plan = relationship("MealPlan")
    user = relationship("User", back_populates="meal_tracking")

