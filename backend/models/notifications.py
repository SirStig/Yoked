from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Boolean, UUID, func
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    type = Column(String, nullable=False)  # e.g., "message", "friend_request", "like", "comment", "system"
    content = Column(Text, nullable=False)  # e.g., "John liked your post."

    related_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"),
                             nullable=True)  # User who triggered the notification
    related_post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"),
                             nullable=True)  # Post related to the notification
    related_reel_id = Column(UUID(as_uuid=True), ForeignKey("reels.id"),
                             nullable=True)  # Reel related to the notification
    related_workout_id = Column(UUID(as_uuid=True), ForeignKey("workouts.id"),
                                nullable=True)  # Workout related to the notification

    is_read = Column(Boolean, default=False)  # Tracks if the user has seen the notification
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
    related_user = relationship("User", foreign_keys=[related_user_id])  # User who triggered the action
    related_post = relationship("Post")
    related_reel = relationship("Reel")
    related_workout = relationship("Workout")
