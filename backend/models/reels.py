import enum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, UUID, func
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime

from backend.models.tags import reel_tags

# Association table for reel likes
reel_likes = Table(
    "reel_likes",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("reel_id", UUID, ForeignKey("reels.id"), primary_key=True),
)

# Association table for reel bookmarks (saved videos)
reel_bookmarks = Table(
    "reel_bookmarks",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("reel_id", UUID, ForeignKey("reels.id"), primary_key=True),
)

class Reel(Base):
    __tablename__ = "reels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Video storage (Vimeo) & Thumbnail (AWS S3)
    video_vimeo_url = Column(String, nullable=False)  # Vimeo link
    thumbnail_s3_url = Column(String, nullable=True)  # AWS S3 for thumbnail storage

    description = Column(Text, nullable=True)

    # Engagement metrics
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)  # Track video views

    # Ad system (For free users)
    is_advertisement = Column(Boolean, default=False)  # Determines if reel is an ad

    # Hashtags & Categories
    tags = relationship("Tag", secondary=reel_tags, back_populates="reels")

    # Privacy & Moderation
    is_reported = Column(Boolean, default=False)  # Flagged for moderation
    visibility = Column(String, default="public")  # Options: public, friends-only, private

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = relationship("User", back_populates="reels")
    likes = relationship("User", secondary=reel_likes, back_populates="liked_reels")
    bookmarks = relationship("User", secondary=reel_bookmarks, back_populates="bookmarked_reels")
    comments = relationship("ReelComment", back_populates="reel", cascade="all, delete-orphan")


class ReelComment(Base):
    __tablename__ = "reel_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Text, nullable=False)
    reel_id = Column(UUID(as_uuid=True), ForeignKey("reels.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    likes_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reel = relationship("Reel", back_populates="comments")
    author = relationship("User", back_populates="reel_comments")


class ReportedReel(Base):
    __tablename__ = "reported_reels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    reel_id = Column(UUID(as_uuid=True), ForeignKey("reels.id"), nullable=False)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reel = relationship("Reel")
    reporter = relationship("User")
