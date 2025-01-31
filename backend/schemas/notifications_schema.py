from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    type: str
    content: str


class NotificationOut(NotificationBase):
    id: UUID4
    user_id: UUID4
    related_user_id: Optional[UUID4] = None
    related_post_id: Optional[UUID4] = None
    related_reel_id: Optional[UUID4] = None
    related_workout_id: Optional[UUID4] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
