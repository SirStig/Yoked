from pydantic import BaseModel, UUID4, Field
from typing import List, Optional
from datetime import datetime


class NutritionArticleBase(BaseModel):
    title: str
    content: str
    category: str
    # noinspection PyDataclass
    tags: List[str] = Field(default_factory=list, description="Tags for searchability")


class NutritionArticleOut(NutritionArticleBase):
    id: UUID4
    author_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MealPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    diet_type: str
    total_calories: int
    protein_grams: Optional[int] = None
    carb_grams: Optional[int] = None
    fat_grams: Optional[int] = None


class MealPlanOut(MealPlanBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserMealTracking(BaseModel):
    id: UUID4
    user_id: UUID4
    meal_plan_id: Optional[UUID4] = None
    date_tracked: datetime
    calories_consumed: int
    protein_grams: Optional[int] = None
    carb_grams: Optional[int] = None
    fat_grams: Optional[int] = None

    class Config:
        from_attributes = True
