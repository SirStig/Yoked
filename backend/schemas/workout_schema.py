from pydantic import BaseModel, HttpUrl
from typing import Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class WorkoutCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty: DifficultyLevel
    duration: int
    equipment: Optional[str] = None
    video_url: HttpUrl

class WorkoutResponse(WorkoutCreate):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True
