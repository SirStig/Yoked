from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ProgressPhoto(BaseModel):
    id: int
    url: str
    uploaded_at: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    friends: List[int]
    progress_photos: List[ProgressPhoto] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


class UserProfile(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    fitness_goals: Optional[str] = None

    class Config:
        orm_mode = True

class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    fitness_goals: Optional[str] = None