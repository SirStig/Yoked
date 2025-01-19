import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from backend.core.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_mobile = Column(Boolean, default=False, nullable=False)  # Indicates if session is mobile

    user = relationship("User", back_populates="sessions")
