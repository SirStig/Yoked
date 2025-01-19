from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum



class Token(BaseModel):
    access_token: str
    token_type: str

class ActivityLevel(str, Enum):
    sedentary = "Sedentary"
    lightly_active = "Lightly Active"
    active = "Active"
    very_active = "Very Active"

class ProgressPhoto(BaseModel):
    id: int
    url: str
    uploaded_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    avatar: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    fitness_goals: Optional[str] = None
    accepted_terms: bool = Field(..., description="User must accept terms and conditions")
    accepted_privacy_policy: bool = Field(..., description="User must accept the privacy policy")

    class Config:
        orm_mode = True

class UserOut(UserBase):
    id: UUID  # Change id to UUID
    is_active: bool
    is_verified: bool
    full_name: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    fitness_goals: Optional[str] = None
    friends: List[UUID]  # Assuming friends are UUIDs now
    progress_photos: Optional[List[ProgressPhoto]] = None
    subscription_plan: Optional[str] = None

    class Config:
        orm_mode = True

class UserProfile(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    fitness_goals: Optional[str] = None
    full_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None
    subscription_plan: Optional[str] = None
    joined_at: datetime
    setup_step: str
    is_verified: bool
    id: UUID

    class Config:
        orm_mode = True
        from_attributes = True

class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    fitness_goals: Optional[str] = None  # Correct alignment
    profile_picture: Optional[str] = None
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[str]
    weight: Optional[str]
    height_unit: Optional[str] = None
    weight_unit: Optional[str] = None
    setup_step: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str
    is_mobile: bool = False