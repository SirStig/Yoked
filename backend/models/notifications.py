from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # User receiving the notification
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="notifications", foreign_keys=[user_id])

    # User who triggered the notification (e.g., who liked the post)
    related_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    related_user = relationship("User", foreign_keys=[related_user_id])

    type = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    # Related objects (only one will be filled depending on type)
    related_post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=True)
    related_post = relationship("Post")

    related_reel_id = Column(UUID(as_uuid=True), ForeignKey("reels.id"), nullable=True)
    related_reel = relationship("Reel")

    related_workout_id = Column(UUID(as_uuid=True), ForeignKey("workouts.id"), nullable=True)
    related_workout = relationship("Workout")

    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
