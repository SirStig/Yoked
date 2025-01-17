from pydantic import BaseModel
from typing import List

class CommentBase(BaseModel):
    content: str

class CommentOut(CommentBase):
    id: int
    post_id: int
    author_id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostOut(PostBase):
    id: int
    author_id: int
    likes: int
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True
