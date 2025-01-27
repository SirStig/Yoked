import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base
from unittest.mock import patch
import stripe

# PostgreSQL Test Database URL
TEST_DATABASE_URL = "postgresql://postgres:7V4rEHT93gNp6.jhMAiW7ursogE4j!@localhost:5432/project-yoked-test"

# Set up the PostgreSQL test database engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    """
    Set up the PostgreSQL database for testing, create tables, and provide teardown.
    """
    # Create all tables in the PostgreSQL test database
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop tables after all tests are done
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    """
    Provide a transactional PostgreSQL database session for each test.
    """
    connection = test_db.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session  # Provide the session to the test

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def mock_stripe(mocker):
    """
    Mock Stripe API calls to avoid hitting the real API.
    """
    mocker.patch.object(stripe.Subscription, "retrieve", return_value={
        "id": "sub_123",
        "status": "active",
        "items": {
            "data": [{
                "price": {
                    "id": "price_123",
                }
            }]
        },
        "current_period_end": 1700000000  # Example timestamp
    })

    mocker.patch.object(stripe.Subscription, "modify", return_value={
        "id": "sub_123",
        "status": "active",
        "current_period_end": 1700000000  # Example timestamp
    })

    mocker.patch.object(stripe.Subscription, "delete", return_value={"id": "sub_123", "status": "canceled"})
