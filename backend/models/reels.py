from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Reel(Base):
    __tablename__ = "reels"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    likes = Column(Integer, default=0)
    comments = relationship("ReelComment", back_populates="reel")

class ReelComment(Base):
    __tablename__ = "reel_comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    reel_id = Column(Integer, ForeignKey("reels.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reel = relationship("Reel", back_populates="comments")
