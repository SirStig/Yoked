import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from backend.core.database import Base, get_db
from backend.models.user import User, UserType
from backend.core.config import settings  # Import TEST_DATABASE_URL
from backend.api.auth.auth_service import get_current_user
from uuid import uuid4
from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app

# PostgreSQL engine for the test database
engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the test database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Drop and recreate tables before the test session starts
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Fixture to provide a clean database session for each test
@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# Mock user fixture
@pytest.fixture
def mock_user(db_session):
    # Ensure a clean slate before creating the user
    db_session.query(User).delete()
    user = User(
        id=uuid4(),
        full_name="Test User",
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
        user_type=UserType.REGULAR,
        subscription_plan="Free",
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
        profile_version=1,
    )
    db_session.add(user)
    db_session.commit()
    return user


# Override get_db dependency globally
@pytest.fixture(autouse=True)
def override_get_db(db_session):
    app.dependency_overrides[get_db] = lambda: db_session


# Override get_current_user dependency globally
@pytest.fixture(autouse=True)
def override_get_current_user(mock_user):
    app.dependency_overrides[get_current_user] = lambda: mock_user


# Test client fixture
@pytest.fixture
def client():
    return TestClient(app)
