from pydantic import BaseModel, UUID4, Field
from typing import List
from datetime import datetime


class AchievementBase(BaseModel):
    name: str
    description: str
    icon_url: Optional[str] = None


class AchievementOut(AchievementBase):
    id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True


class UserAchievementOut(BaseModel):
    id: UUID4
    user_id: UUID4
    achievement_id: UUID4
    earned_at: datetime

    class Config:
        from_attributes = True


class UserLevelOut(BaseModel):
    id: UUID4
    user_id: UUID4
    level: int
    experience_points: int
    next_level_xp: int
    updated_at: datetime

    class Config:
        from_attributes = True


class LeaderboardOut(BaseModel):
    id: UUID4
    user_id: UUID4
    total_points: int
    rank: int
    updated_at: datetime

    class Config:
        from_attributes = True
