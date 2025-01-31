# backend/models/tags.py
from sqlalchemy import Column, String, Table, ForeignKey, UUID
from sqlalchemy.orm import relationship
from backend.core.database import Base

# Association tables for tags in different models
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", UUID, ForeignKey("posts.id"), primary_key=True),
    Column("tag", String, ForeignKey("tags.tag"), primary_key=True),
)

reel_tags = Table(
    "reel_tags",
    Base.metadata,
    Column("reel_id", UUID, ForeignKey("reels.id"), primary_key=True),
    Column("tag", String, ForeignKey("tags.tag"), primary_key=True),
)

workout_tags = Table(
    "workout_tags",
    Base.metadata,
    Column("workout_id", UUID, ForeignKey("workouts.id"), primary_key=True),
    Column("tag", String, ForeignKey("tags.tag"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    tag = Column(String, primary_key=True)

    # Relationships to other models
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
    reels = relationship("Reel", secondary=reel_tags, back_populates="tags")
    workouts = relationship("Workout", secondary=workout_tags, back_populates="tags")
