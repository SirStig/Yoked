import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from backend.core.database import Base

class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_mobile = Column(Boolean, default=False, nullable=False)
    mfa_verified = Column(Boolean, default=False)

    # New fields for session tracking
    device_type = Column(String, nullable=True)
    location = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
