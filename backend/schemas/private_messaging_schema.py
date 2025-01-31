from pydantic import BaseModel, UUID4, Field
from typing import List, Optional
from datetime import datetime


class ChatBase(BaseModel):
    is_group_chat: bool


class ChatOut(ChatBase):
    id: UUID4
    participants: List[UUID4]
    created_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    content: Optional[str] = None
    image_s3_url: Optional[str] = None
    video_vimeo_url: Optional[str] = None


class MessageOut(MessageBase):
    id: UUID4
    chat_id: UUID4
    sender_id: UUID4
    is_edited: bool
    is_deleted: bool
    read_by: List[UUID4] = []
    reactions: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TypingStatusOut(BaseModel):
    id: UUID4
    chat_id: UUID4
    user_id: UUID4
    is_typing: bool

    class Config:
        from_attributes = True
