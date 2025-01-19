import pytest
from backend.core.test_database import initialize_test_database, cleanup_test_database, get_test_db
from backend.main import app
from backend.core.database import get_db

# Override FastAPI dependency to use the test database
def override_get_db():
    yield from get_test_db()

app.dependency_overrides[get_db] = override_get_db

# Test database setup and teardown
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    print("Initializing test database...")
    initialize_test_database()
    yield
    print("Cleaning up test database...")
    cleanup_test_database()

# Provide a database session for each test
@pytest.fixture(scope="function")
def db_session():
    from backend.core.test_database import TestingSessionLocal
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
