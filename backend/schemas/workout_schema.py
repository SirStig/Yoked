from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# noinspection PyDataclass
class WorkoutCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = Field(None, description="Subcategory of the workout")
    muscle_groups: List[str] = Field(default_factory=list, description="Muscle groups targeted by this workout")
    difficulty: DifficultyLevel
    duration: int
    equipment: List[str] = Field(default_factory=list, description="Equipment required for the workout")
    video_vimeo_url: str = Field(..., description="Vimeo video link for the workout")

    class Config:
        from_attributes = True


# noinspection PyDataclass
class WorkoutOut(WorkoutCreate):
    id: UUID4
    times_completed: int = Field(0, description="Number of times this workout has been completed")
    likes_count: int = Field(0, description="Number of likes on this workout")
    bookmarks_count: int = Field(0, description="Number of users who have bookmarked this workout")
    views_count: int = Field(0, description="Number of views on this workout")
    bookmarked_by: List[UUID4] = Field(default_factory=list, description="List of user IDs who bookmarked this workout")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkoutProgress(BaseModel):
    id: UUID4
    user_id: UUID4
    workout_id: UUID4
    completed_at: datetime

    class Config:
        from_attributes = True
