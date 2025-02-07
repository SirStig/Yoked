from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from backend.core.config import settings

# Production database URL
DATABASE_URL = settings.DATABASE_URL

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()

from backend.models.notifications import *
from backend.models.reels import *
from backend.models.tags import *
from backend.models.workout import *
from backend.models.nutrition import *
from backend.models.community_post import *
from backend.models.private_messaging import *
from backend.models.gamification import *
from backend.models.payment import *
from backend.models.session import *
from backend.models.subscription_tier import *
from backend.models.user import *

# Dependency for production database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database (for production)
def init_db():
    from backend.models import user  # Import all models here
    Base.metadata.create_all(bind=engine)
