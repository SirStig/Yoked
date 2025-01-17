from pydantic import BaseModel
from typing import List

class ReelCommentBase(BaseModel):
    content: str

class ReelCommentOut(ReelCommentBase):
    id: int
    reel_id: int
    author_id: int

    class Config:
        orm_mode = True

class ReelBase(BaseModel):
    url: str
    description: str

class ReelOut(ReelBase):
    id: int
    author_id: int
    likes: int
    comments: List[ReelCommentOut] = []

    class Config:
        orm_mode = True
