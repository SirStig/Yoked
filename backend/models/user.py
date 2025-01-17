from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.core.database import Base

# Association table for friends
user_friends = Table(
    "user_friends",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("friend_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String, nullable=True)  # Stores S3 URL
    fitness_goals = Column(String, nullable=True)