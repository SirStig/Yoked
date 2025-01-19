from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.core.config import settings

# Create engine for test database
test_engine = create_engine(settings.TEST_DATABASE_URL, pool_pre_ping=True)

# Session management for test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Declarative base for models (reuse production base)
Base = declarative_base()

# Initialize the test database
def initialize_test_database():
    """Create all tables in the test database."""
    from backend.models.user import User  # Import models
    Base.metadata.create_all(bind=test_engine)

# Clean up the test database
def cleanup_test_database():
    """Drop all tables in the test database."""
    Base.metadata.drop_all(bind=test_engine)

# Dependency for getting a test database session
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
