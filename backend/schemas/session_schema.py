from pydantic import BaseModel, UUID4, Field
from datetime import datetime
from typing import Optional


class UserSession(BaseModel):
    id: UUID4 = Field(..., description="Unique session ID")
    user_id: UUID4 = Field(..., description="ID of the user who owns the session")
    token: str = Field(..., description="Session token")
    created_at: datetime = Field(..., description="Time the session was created")
    expires_at: datetime = Field(..., description="Time the session expires")
    is_mobile: bool = Field(..., description="Indicates if the session is from a mobile device")
    mfa_verified: bool = Field(..., description="Indicates if the session is MFA verified")
    is_active: bool = Field(..., description="Indicates if the session is active")

    # Device Information
    device_type: Optional[str] = Field(None, description="Type of device used for the session (e.g., mobile, desktop)")
    device_os: Optional[str] = Field(None, description="Operating system of the device (e.g., iOS, Windows)")
    browser: Optional[str] = Field(None, description="Browser used for the session (e.g., Chrome, Safari)")

    # Security & Activity
    location: Optional[str] = Field(None, description="Location of the session (e.g., city, country)")
    ip_address: Optional[str] = Field(None, description="IP address of the session")
    last_activity: datetime = Field(..., description="Last activity time for the session")

    class Config:
        from_attributes = True
