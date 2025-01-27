from uuid import uuid4
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.api.subscriptions.subscription_routes import router
from backend.main import app
from backend.models.subscription_tier import SubscriptionTier
from backend.models.user import User, UserType
from datetime import datetime

# Add the router to the test app
app.include_router(router)
client = TestClient(app)


# Fixture to create a mock user
@pytest.fixture
def mock_user(db_session):
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
    )
    db_session.add(user)
    db_session.commit()
    return user


# Fixture to create a mock subscription tier
@pytest.fixture
def mock_subscription_tier(db_session):
    tier = SubscriptionTier(
        id=uuid4(),
        name="Pro",
        price=1999,
        currency="USD",
        is_active=True,
        recurring_interval="monthly",
        features=["Access to workouts", "Community posts"],
        version=1,
    )
    db_session.add(tier)
    db_session.commit()
    return tier


# Test: List Subscription Tiers
def test_list_subscription_tiers(mock_subscription_tier, db_session):
    with patch("backend.api.subscriptions.subscription_routes.get_db", return_value=db_session):
        response = client.get("/api/subscriptions/")
        assert response.status_code == 200
        tiers = response.json()
        assert len(tiers) == 1
        assert tiers[0]["name"] == mock_subscription_tier.name
        assert tiers[0]["price"] == mock_subscription_tier.price
        assert tiers[0]["currency"] == mock_subscription_tier.currency
        assert tiers[0]["is_active"] is True
        assert tiers[0]["features"] == ["Access to workouts", "Community posts"]


# Test: Retrieve Subscription Tier by ID
def test_retrieve_subscription_tier(mock_subscription_tier, db_session):
    with patch("backend.api.subscriptions.subscription_routes.get_db", return_value=db_session):
        response = client.get(f"/api/subscriptions/{mock_subscription_tier.id}")
        assert response.status_code == 200
        tier = response.json()
        assert tier["name"] == mock_subscription_tier.name
        assert tier["price"] == mock_subscription_tier.price
        assert tier["currency"] == mock_subscription_tier.currency


# Test: Create a Subscription Tier
@patch("backend.api.subscriptions.subscription_service.create_subscription_tier")
def test_create_subscription_tier(mock_create_tier, db_session):
    mock_create_tier.return_value = SubscriptionTier(
        id=uuid4(),
        name="Elite",
        price=2999,
        currency="USD",
        is_active=True,
        recurring_interval="monthly",
        features=["Ad-free reels", "Live classes"],
        version=1,
    )

    payload = {
        "name": "Elite",
        "price": 2999,
        "currency": "USD",
        "is_active": True,
        "recurring_interval": "monthly",
        "features": ["Ad-free reels", "Live classes"],
    }

    with patch("backend.api.subscriptions.subscription_routes.get_db", return_value=db_session):
        response = client.post("/api/subscriptions/", json=payload)
        assert response.status_code == 200
        tier = response.json()
        assert tier["name"] == "Elite"
        assert tier["price"] == 2999
        assert tier["currency"] == "USD"
        assert tier["features"] == ["Ad-free reels", "Live classes"]


# Test: Update a Subscription Tier
@patch("backend.api.subscriptions.subscription_service.update_subscription_tier")
def test_update_subscription_tier(mock_update_tier, mock_subscription_tier, db_session):
    mock_update_tier.return_value = mock_subscription_tier
    payload = {"name": "Pro+", "price": 2499, "features": ["Updated Feature"]}

    with patch("backend.api.subscriptions.subscription_routes.get_db", return_value=db_session):
        response = client.put(f"/api/subscriptions/{mock_subscription_tier.id}", json=payload)
        assert response.status_code == 200
        updated_tier = response.json()
        assert updated_tier["name"] == "Pro+"
        assert updated_tier["price"] == 2499
        assert updated_tier["features"] == ["Updated Feature"]


# Test: Delete a Subscription Tier
@patch("backend.api.subscriptions.subscription_service.delete_subscription_tier")
def test_delete_subscription_tier(mock_delete_tier, mock_subscription_tier, db_session):
    mock_delete_tier.return_value = None

    with patch("backend.api.subscriptions.subscription_routes.get_db", return_value=db_session):
        response = client.delete(f"/api/subscriptions/{mock_subscription_tier.id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Subscription tier deleted successfully."


# Test: Deactivate a Subscription Tier
@patch("backend.api.subscriptions.subscription_service.deactivate_subscription_tier")
def test_deactivate_subscription_tier(mock_deactivate_tier, mock_subscription_tier, db_session):
    mock_deactivate_tier.return_value = None

    with patch("backend.api.subscriptions.subscription_routes.get_db", return_value=db_session):
        response = client.put(f"/api/subscriptions/{mock_subscription_tier.id}/deactivate")
        assert response.status_code == 200
        assert response.json()["message"] == "Subscription tier deactivated successfully."
