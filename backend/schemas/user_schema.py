from pydantic import BaseModel, Field, EmailStr, UUID4, PositiveInt
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
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

# Progress Photos Schema
class ProgressPhoto(BaseModel):
    id: UUID4
    url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Notification Preferences
class NotificationPreferences(BaseModel):
    email_notifications: bool = Field(..., description="Whether the user receives email notifications")
    push_notifications: bool = Field(..., description="Whether the user receives push notifications")

# **🔹 New Additions**
class Token(BaseModel):
    """ Schema for authentication tokens """
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    """ Schema for user login request """
    email: EmailStr
    password: str
    otp: Optional[str] = None  # MFA authentication if enabled
    is_mobile: bool = False  # Distinguish mobile login

class PasswordResetRequest(BaseModel):
    """ Schema for password reset request """
    token: str
    new_password: str

# **🔹 Main User Schemas**
class UserBase(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the user")
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email of the user")
    bio: Optional[str] = Field(None, description="Bio of the user")
    profile_picture: Optional[str] = Field(None, description="URL of the user's profile picture")
    fitness_goals: Optional[str] = Field(None, description="Fitness goals of the user")

class UserCreate(UserBase):
    """ Schema for user registration """
    password: str = Field(..., description="User's password (hashed before saving)")
    accepted_terms: bool = Field(..., description="User must accept terms and conditions")
    accepted_privacy_policy: bool = Field(..., description="User must accept the privacy policy")
    admin_secret_key: Optional[str] = Field(None, description="Secret key required for creating admin users")
    subscription_plan: Optional[str] = Field("Free", description="Subscription plan of the user")
    setup_step: Optional[SetupStep] = Field(SetupStep.email_verification, description="Current setup step for the user")
    user_type: Optional[UserType] = Field(UserType.REGULAR, description="Type of user (regular or admin)")
    is_active: Optional[bool] = Field(True, description="Is the account active")
    is_verified: Optional[bool] = Field(False, description="Is the user's email verified?")
    activity_level: Optional[ActivityLevel] = Field(None, description="User's activity level")
    height: Optional[float] = Field(None, description="User's height")
    weight: Optional[float] = Field(None, description="User's weight")
    height_unit: Optional[str] = Field("ft/in", description="Unit for height")
    weight_unit: Optional[str] = Field("lbs", description="Unit for weight")
    profile_version: Optional[int] = Field(1, description="Profile version for changes")
    flagged_for_review: Optional[bool] = Field(False, description="Is the user flagged for review?")
    joined_at: Optional[datetime] = Field(None, description="Time the user joined the platform")
    accepted_terms_at: Optional[datetime] = Field(None, description="Time the user accepted terms")
    accepted_privacy_policy_at: Optional[datetime] = Field(None, description="Time the user accepted privacy policy")
    age: Optional[PositiveInt] = Field(None, description="Age of the user")
    gender: Optional[str] = Field(None, description="Gender of the user")
    email_notifications: Optional[bool] = Field(True, description="Email notification preference")
    push_notifications: Optional[bool] = Field(True, description="Push notification preference")

class UserResponse(UserBase):
    """ Schema for user profile response """
    id: UUID4
    is_active: bool
    is_verified: bool
    flagged_for_review: bool
    subscription_plan: Optional[str]
    profile_version: int
    user_type: UserType
    joined_at: datetime
    friends: List[UUID4] = Field(default_factory=list, description="List of friend IDs")
    followers: List[UUID4] = Field(default_factory=list, description="List of follower IDs")
    following: List[UUID4] = Field(default_factory=list, description="List of users this user is following")
    friend_requests_sent: List[UUID4] = Field(default_factory=list, description="List of sent friend requests")
    friend_requests_received: List[UUID4] = Field(default_factory=list, description="List of received friend requests")
    progress_photos: Optional[List[ProgressPhoto]] = Field(default_factory=list, description="List of progress photos uploaded by the user")
    email_notifications: bool
    push_notifications: bool
    mfa_enabled: bool = Field(..., description="Indicates if MFA is enabled")
    mfa_secret: Optional[str] = Field(None, description="MFA secret key for TOTP")
    mfa_backup_codes: Optional[List[str]] = Field(None, description="Backup codes for MFA")

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """ Schema for updating user details """
    full_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    fitness_goals: Optional[str] = None
    activity_level: Optional[ActivityLevel] = None
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    profile_version: int = Field(..., description="Must be incremented on update")

class UserSecurityUpdate(BaseModel):
    """ Schema for updating security settings """
    current_password: str
    new_password: str
    enable_mfa: Optional[bool] = None  # Toggle MFA setting

class UserPreferencesUpdate(BaseModel):
    """ Schema for user preferences/settings updates """
    email_notifications: Optional[bool] = True
    push_notifications: Optional[bool] = True
    dark_mode: Optional[bool] = False

class UserMFASetup(BaseModel):
    """ Schema for setting up MFA """
    user_id: UUID4
    mfa_secret: str
    totp_code: str  # The verification code from the user

class UserMFAVerify(BaseModel):
    """ Schema for verifying MFA during login or security checks """
    session_token: str
    user_id: UUID4
    totp_code: str

# **🔹 Notification Preferences Schema**
class NotificationPreferences(BaseModel):
    email_notifications: bool = Field(..., description="User's preference for email notifications")
    push_notifications: bool = Field(..., description="User's preference for push notifications")

# **🔹 User Profile Update Schema**
class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    fitness_goals: Optional[str] = None

# **🔹 Privacy Settings Schema**
class PrivacySettings(BaseModel):
    profile_visibility: str = Field(..., description="User's profile visibility setting")
    blocked_users: List[UUID4] = Field(default_factory=list, description="List of blocked user IDs")
    data_sharing: bool = Field(..., description="Whether user allows data sharing")

# **🔹 Security Settings Schema**
class SecuritySettings(BaseModel):
    mfa_enabled: bool = Field(..., description="Whether multi-factor authentication is enabled")
    login_alerts: bool = Field(..., description="Whether login alerts are enabled")

# **🔹 Theme Preferences Schema**
class ThemePreferences(BaseModel):
    dark_mode: bool = Field(..., description="Whether dark mode is enabled")
    font_size: Optional[str] = Field(None, description="User's preferred font size")

# **🔹 Third-Party Accounts Schema**
class ThirdPartyAccounts(BaseModel):
    google_connected: bool = Field(..., description="Whether Google account is connected")
    apple_connected: bool = Field(..., description="Whether Apple account is connected")

# **🔹 User Profile Schema**
class UserProfile(BaseModel):
    """ Schema for retrieving and updating user profile details. """
    id: UUID4
    full_name: Optional[str] = Field(None, description="Full name of the user")
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="User's email")
    bio: Optional[str] = Field(None, description="User bio")
    profile_picture: Optional[str] = Field(None, description="Profile picture URL")
    fitness_goals: Optional[str] = Field(None, description="User fitness goals")
    activity_level: Optional[str] = Field(None, description="User activity level")
    height: Optional[float] = Field(None, description="User height")
    weight: Optional[float] = Field(None, description="User weight")
    profile_version: int = Field(..., description="Profile version for tracking changes")
    joined_at: datetime = Field(..., description="User account creation date")

    class Config:
        from_attributes = True