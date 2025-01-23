from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, PositiveFloat, PositiveInt
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


class UserType(str, Enum):
    REGULAR = "regular"
    ADMIN = "admin"


class SetupStep(str, Enum):
    email_verification = "verify_email"
    profile_completion = "profile_completion"
    subscription_selection = "subscription_selection"
    completed = "completed"


class ProgressPhoto(BaseModel):
    id: int
    url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the user")
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email of the user")
    bio: Optional[str] = Field(None, description="Bio of the user")
    profile_picture: Optional[str] = Field(None, description="URL of the user's profile picture")
    fitness_goals: Optional[str] = Field(None, description="Fitness goals of the user")


class UserCreate(UserBase):
    hashed_password: str = Field(..., description="Password of the user")
    accepted_terms: bool = Field(..., description="User must accept terms and conditions")
    accepted_privacy_policy: bool = Field(..., description="User must accept the privacy policy")
    admin_secret_key: Optional[str] = Field(
        None, description="Secret key required for creating admin users"
    )
    subscription_plan: Optional[str] = Field(
        "Free", description="Subscription plan of the user"
    )
    setup_step: Optional[SetupStep] = Field(
        SetupStep.email_verification, description="Current setup step for the user"
    )
    user_type: Optional[UserType] = Field(
        UserType.REGULAR, description="Type of user (regular or admin)"
    )
    is_active: Optional[bool] = Field(True, description="Is the account active")
    is_verified: Optional[bool] = Field(False, description="Is the user's email verified?")
    activity_level: Optional[ActivityLevel] = Field(
        None, description="User's activity level"
    )
    height: Optional[float] = Field(None, description="User's height")
    weight: Optional[float] = Field(None, description="User's weight")
    height_unit: Optional[str] = Field("ft/in", description="Unit for height")
    weight_unit: Optional[str] = Field("lbs", description="Unit for weight")
    profile_version: Optional[int] = Field(1, description="Profile version for changes")
    flagged_for_review: Optional[bool] = Field(False, description="Is the user flagged for review?")
    joined_at: Optional[datetime] = Field(
        None, description="Time the user joined the platform"
    )
    accepted_terms_at: Optional[datetime] = Field(None, description="Time the user accepted terms")
    accepted_privacy_policy_at: Optional[datetime] = Field(
        None, description="Time the user accepted privacy policy"
    )
    age: Optional[PositiveInt] = Field(None, description="Age of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")


# noinspection PyDataclass
class UserOut(UserBase):
    id: UUID
    is_active: bool = Field(..., description="Whether the user account is active")
    is_verified: bool = Field(..., description="Whether the user has verified their email")
    flagged_for_review: bool = Field(..., description="Indicates if the user is flagged for review")
    subscription_plan: Optional[str] = Field(None, description="Subscription plan of the user")
    profile_version: int = Field(..., description="Version of the user's profile")
    user_type: UserType = Field(..., description="Type of user (regular or admin)")
    joined_at: datetime = Field(..., description="Date and time the user joined")
    friends: List[UUID] = Field(default_factory=list, description="List of friend IDs")
    progress_photos: Optional[List[ProgressPhoto]] = Field(default_factory=list, description="List of progress photos uploaded by the user")

    class Config:
        from_attributes = True


# noinspection PyDataclass
class UserProfile(UserBase):
    age: Optional[PositiveInt] = Field(None, description="Age of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    activity_level: Optional[ActivityLevel] = Field(None, description="Activity level of the user")
    height: Optional[PositiveFloat] = Field(None, description="Height of the user")
    weight: Optional[PositiveFloat] = Field(None, description="Weight of the user")
    height_unit: Optional[str] = Field(None, description="Unit for height")
    weight_unit: Optional[str] = Field(None, description="Unit for weight")
    setup_step: Optional[SetupStep] = Field(
        SetupStep.email_verification, description="Current setup step of the user"
    )
    is_active: bool = Field(..., description="Whether the user account is active")
    is_verified: bool = Field(..., description="Whether the user has verified their email")
    flagged_for_review: bool = Field(..., description="Indicates if the user is flagged for review")
    profile_version: int = Field(..., description="Version of the user's profile")
    joined_at: datetime = Field(..., description="Date and time the user joined")
    user_type: UserType = Field(..., description="Type of user (regular or admin)")
    friends: List[UUID] = Field(default_factory=list, description="List of friend IDs")
    progress_photos: Optional[List[ProgressPhoto]] = Field(default_factory=list, description="List of progress photos uploaded by the user")

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the user")
    bio: Optional[str] = Field(None, description="Bio of the user")
    fitness_goals: Optional[str] = Field(None, description="Fitness goals of the user")
    profile_picture: Optional[str] = Field(None, description="URL of the user's profile picture")
    age: Optional[PositiveInt] = Field(None, description="Age of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    height: Optional[PositiveFloat] = Field(None, description="Height of the user")
    weight: Optional[PositiveFloat] = Field(None, description="Weight of the user")
    height_unit: Optional[str] = Field(None, description="Unit for height")
    weight_unit: Optional[str] = Field(None, description="Unit for weight")
    activity_level: Optional[ActivityLevel] = Field(None, description="Activity level of the user")
    setup_step: Optional[SetupStep] = Field(None, description="Current setup step of the user")

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email for login")
    password: str = Field(..., description="Password for login")
    is_mobile: bool = Field(False, description="Indicates if login is from a mobile device")

class UserMFASetup(BaseModel):
    user_id: UUID = Field(..., description="User ID of the admin")
    mfa_secret: str = Field(..., description="MFA secret key for setup")
    totp_code: str = Field(..., description="One-time TOTP code for verification")

class UserMFAVerify(BaseModel):
    user_id: UUID = Field(..., description="User ID of the admin")
    totp_code: str = Field(..., description="One-time TOTP code for verification")

class AdminUserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the admin user")
    username: Optional[str] = Field(None, description="Username of the admin user")
    email: Optional[EmailStr] = Field(None, description="Email of the admin user")
    is_active: Optional[bool] = Field(None, description="Whether the admin account is active")
    user_type: Optional[UserType] = Field(None, description="Type of user (regular or admin)")
    admin_secret_key: Optional[str] = Field(None, description="Secret key for admin users")
    flagged_for_review: Optional[bool] = Field(None, description="Indicates if the admin is flagged for review")

    class Config:
        from_attributes = True
