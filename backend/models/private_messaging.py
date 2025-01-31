from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, UUID, func, ARRAY
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime

# Association table for group chat participants
group_chat_participants = Table(
    "group_chat_participants",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("chat_id", UUID, ForeignKey("chats.id"), primary_key=True),
)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    is_group_chat = Column(Boolean, default=False)  # True for group chats, False for one-on-one
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    participants = relationship("User", secondary=group_chat_participants, back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=True)

    # Media Attachments (AWS S3 for images, Vimeo for videos)
    image_s3_url = Column(String, nullable=True)
    video_vimeo_url = Column(String, nullable=True)

    # Message Features
    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    read_by = Column(ARRAY(UUID), nullable=True)  # List of users who have read the message
    reactions = Column(ARRAY(String), nullable=True)  # List of emoji reactions

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages_sent")


class TypingStatus(Base):
    __tablename__ = "typing_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_typing = Column(Boolean, default=False)

    chat = relationship("Chat")
    user = relationship("User")
