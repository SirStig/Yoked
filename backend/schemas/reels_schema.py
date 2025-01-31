from pydantic import BaseModel, UUID4, Field
from typing import List, Optional
from datetime import datetime


class ReelCommentBase(BaseModel):
    content: str


class ReelCommentOut(ReelCommentBase):
    id: UUID4
    reel_id: UUID4
    author_id: UUID4
    likes_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReelBase(BaseModel):
    description: str


# noinspection PyDataclass
class ReelOut(ReelBase):
    id: UUID4
    author_id: UUID4
    video_vimeo_url: str = Field(..., description="Vimeo video link for the reel")
    thumbnail_s3_url: Optional[str] = Field(None, description="S3 thumbnail image link")
    likes_count: int
    shares_count: int
    comments_count: int
    views_count: int
    is_advertisement: bool
    advertiser_id: Optional[UUID4] = Field(None, description="ID of the advertiser if this is an ad")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the reel")
    created_at: datetime
    updated_at: datetime
    comments: List[ReelCommentOut] = []

    class Config:
        from_attributes = True
