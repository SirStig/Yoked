from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Table, UUID, func
from sqlalchemy.orm import relationship
from backend.core.database import Base
import uuid
from datetime import datetime

from backend.models.tags import post_tags

# Association table for post likes
post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("post_id", UUID, ForeignKey("posts.id"), primary_key=True),
)

# Association table for post bookmarks
post_bookmarks = Table(
    "post_bookmarks",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("post_id", UUID, ForeignKey("posts.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Media Storage (AWS S3 for images, Vimeo for videos)
    image_s3_url = Column(String, nullable=True)  # Stores image URL from AWS S3
    video_vimeo_url = Column(String, nullable=True)  # Stores Vimeo link

    # Engagement Metrics
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)  # Track views for analytics

    # Hashtags & Categories
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

    # Moderation & Privacy
    is_pinned = Column(Boolean, default=False)  # For admin-pinned posts
    is_reported = Column(Boolean, default=False)  # Marked for moderation
    visibility = Column(String, default="public")  # Options: public, friends-only, private

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = relationship("User", back_populates="posts")
    likes = relationship("User", secondary=post_likes, back_populates="liked_posts")
    bookmarks = relationship("User", secondary=post_bookmarks, back_populates="bookmarked_posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    likes_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")


class ReportedPost(Base):
    __tablename__ = "reported_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post")
    reporter = relationship("User")
