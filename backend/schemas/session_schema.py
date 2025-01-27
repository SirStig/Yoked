from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class UserSession(BaseModel):
    id: UUID = Field(..., description="Unique session ID")
    user_id: UUID = Field(..., description="ID of the user who owns the session")
    token: str = Field(..., description="Session token")
    created_at: datetime = Field(..., description="Time the session was created")
    expires_at: datetime = Field(..., description="Time the session expires")
    is_mobile: bool = Field(..., description="Indicates if the session is from a mobile device")
    mfa_verified: bool = Field(..., description="Indicates if the session is MFA verified")
    device_type: str = Field(None, description="Type of device used for the session (e.g., browser, iOS, Android)")
    location: str = Field(None, description="Location of the session (e.g., city, country)")
    ip_address: str = Field(None, description="IP address of the session")
    last_activity: datetime = Field(..., description="Last activity time for the session")

    class Config:
        from_attributes = True
