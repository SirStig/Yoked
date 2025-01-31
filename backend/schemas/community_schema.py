from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime


class CommentBase(BaseModel):
    content: str


class CommentOut(CommentBase):
    id: UUID4
    post_id: UUID4
    author_id: UUID4
    likes_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str


class PostOut(PostBase):
    id: UUID4
    author_id: UUID4
    likes_count: int
    shares_count: int
    comments_count: int
    views_count: int
    is_pinned: bool
    is_reported: bool
    visibility: str
    created_at: datetime
    updated_at: datetime
    comments: List[CommentOut] = []

    class Config:
        from_attributes = True
