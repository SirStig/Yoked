import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from uuid import uuid4
from datetime import datetime
from backend.api.settings.settings_routes import router
from backend.models.user import User, UserType
from backend.schemas.user_schema import NotificationPreferences
from backend.schemas.payment_schema import UpdateSubscription
from backend.main import app

# Add the router to the test app
app.include_router(router)
client = TestClient(app)


# Fixture to mock the current user
@pytest.fixture
def mock_current_user(db_session):
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
        email_notifications=True,
        push_notifications=True,
    )
    db_session.add(user)
    db_session.commit()
    return user


# Test fetching notification preferences
def test_get_notification_preferences(mock_current_user, db_session):
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        response = client.get("/api/settings/notifications")
        assert response.status_code == 200
        assert response.json() == {
            "email_notifications": True,
            "push_notifications": True,
        }


# Test updating notification preferences
def test_update_notification_preferences(mock_current_user, db_session):
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        payload = {
            "email_notifications": False,
            "push_notifications": True,
        }
        response = client.put("/api/settings/notifications", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Notification preferences updated successfully."

        # Verify the database update
        updated_user = db_session.query(User).filter_by(id=mock_current_user.id).first()
        assert updated_user.email_notifications is False
        assert updated_user.push_notifications is True


# Test resetting MFA
def test_reset_mfa(mock_current_user, db_session):
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        with patch("backend.services.mfa.reset_mfa") as mock_reset_mfa:
            mock_reset_mfa.return_value = None
            response = client.put("/api/settings/reset-mfa")
            assert response.status_code == 200
            assert response.json()["message"] == "MFA reset successfully. Please set up MFA again."


# Test fetching subscription details
def test_get_subscription_details(mock_current_user, db_session):
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        mock_current_user.subscription_plan = "Pro"
        response = client.get("/api/settings/subscription")
        assert response.status_code == 200
        assert response.json()["subscription_name"] == "Pro"


# Test updating subscription
@patch("backend.api.settings.settings_routes.update_user_subscription")
def test_update_subscription(mock_update_subscription, mock_current_user, db_session):
    mock_update_subscription.return_value = None
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        payload = {"subscription_tier_id": "tier-id-123"}
        response = client.put("/api/settings/subscription", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Subscription updated successfully."


# Test canceling subscription
@patch("backend.api.settings.settings_routes.cancel_user_subscription")
def test_cancel_subscription(mock_cancel_subscription, mock_current_user, db_session):
    mock_cancel_subscription.return_value = None
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        response = client.delete("/api/settings/subscription")
        assert response.status_code == 200
        assert response.json()["message"] == "Subscription cancelled successfully."


# Test fetching active sessions
@patch("backend.services.session_service.fetch_user_sessions")
def test_get_user_sessions(mock_fetch_user_sessions, mock_current_user, db_session):
    mock_fetch_user_sessions.return_value = [
        {
            "id": "session-id-123",
            "device_type": "Web",
            "location": "USA",
            "ip_address": "192.168.1.1",
            "created_at": "2025-01-26T12:00:00",
            "expires_at": "2025-01-27T12:00:00",
            "last_activity": "2025-01-26T12:30:00",
        }
    ]
    with patch("backend.api.settings.settings_routes.get_current_user", return_value=mock_current_user):
        response = client.get("/api/settings/sessions")
        assert response.status_code == 200
        sessions = response.json()
        assert len(sessions) == 1
        assert sessions[0]["device_type"] == "Web"
        assert sessions[0]["location"] == "USA"
        assert sessions[0]["ip_address"] == "192.168.1.1"
