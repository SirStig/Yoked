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
