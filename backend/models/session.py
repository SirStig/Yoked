import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from backend.core.database import Base


class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True, nullable=False)

    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_mobile = Column(Boolean, default=False, nullable=False)
    mfa_verified = Column(Boolean, default=False)  # Tracks if session was MFA verified

    # Device & Security Tracking
    device_type = Column(String, nullable=True)  # e.g., "iPhone", "Windows PC"
    device_os = Column(String, nullable=True)  # e.g., "iOS 16", "Windows 11"
    browser = Column(String, nullable=True)  # e.g., "Chrome", "Safari"
    location = Column(String, nullable=True)  # Approximate login location
    ip_address = Column(String, nullable=True)  # User's IP address
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")

    def is_expired(self):
        """Check if session has expired"""
        return datetime.utcnow() > self.expires_at
