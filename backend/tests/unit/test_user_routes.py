from uuid import uuid4
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import datetime
from backend.api.users.user_routes import router
from backend.models.user import User, UserType
from backend.schemas.user_schema import UserProfileUpdate
from backend.core.database import get_db
from backend.main import app

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
        profile_version=1,
    )
    db_session.add(user)
    db_session.commit()
    return user


# Test fetching the user profile
def test_get_profile(mock_user, db_session):
    with patch("backend.api.users.user_routes.get_current_user", return_value=mock_user):
        response = client.get("/profile")
        assert response.status_code == 200
        profile = response.json()
        assert profile["username"] == mock_user.username
        assert profile["email"] == mock_user.email
        assert profile["full_name"] == mock_user.full_name
        assert profile["profile_version"] == mock_user.profile_version


# Test fetching the profile version
def test_get_profile_version(mock_user, db_session):
    with patch("backend.api.users.user_routes.get_current_user", return_value=mock_user):
        response = client.get("/profile/version")
        assert response.status_code == 200
        assert response.json()["profile_version"] == mock_user.profile_version


# Test updating the user profile
def test_update_profile(mock_user, db_session):
    with patch("backend.api.users.user_routes.get_current_user", return_value=mock_user):
        payload = {
            "full_name": "Updated Test User",
            "bio": "New bio description",
        }
        response = client.put("/profile", json=payload)
        assert response.status_code == 200
        updated_profile = response.json()
        assert updated_profile["full_name"] == "Updated Test User"
        assert updated_profile["bio"] == "New bio description"
        assert updated_profile["profile_version"] == mock_user.profile_version + 1


# Test deactivating the user account
def test_deactivate_account(mock_user, db_session):
    with patch("backend.api.users.user_routes.get_current_user", return_value=mock_user):
        response = client.put("/deactivate")
        assert response.status_code == 200
        assert response.json()["message"] == "Account deactivated successfully"
        deactivated_user = db_session.query(User).filter_by(id=mock_user.id).first()
        assert deactivated_user.is_active is False
        assert deactivated_user.profile_version == mock_user.profile_version + 1


# Test reactivating the user account
def test_reactivate_account(mock_user, db_session):
    mock_user.is_active = False
    db_session.commit()

    with patch("backend.api.users.user_routes.reactivate_user") as mock_reactivate_user:
        mock_reactivate_user.return_value = None
        response = client.put(f"/reactivate?user_id={mock_user.id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Account reactivated successfully"

        reactivated_user = db_session.query(User).filter_by(id=mock_user.id).first()
        assert reactivated_user.is_active is True
        assert reactivated_user.profile_version == mock_user.profile_version + 1


# Test checking active status
def test_check_active_status(mock_user, db_session):
    with patch("backend.api.users.user_routes.get_current_user", return_value=mock_user):
        response = client.get("/active-status")
        assert response.status_code == 200
        assert response.json()["is_active"] is True
