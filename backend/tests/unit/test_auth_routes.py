import pytest
from uuid import uuid4
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import datetime
from backend.api.auth.auth_routes import router
from backend.main import app
from backend.models.user import User, UserType

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
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
    )
    db_session.add(user)
    db_session.commit()
    return user


# Test user registration
@patch("backend.api.auth.auth_service.create_user")
@patch("backend.api.auth.auth_routes.send_email")
def test_register_user(mock_send_email, mock_create_user, db_session):
    mock_create_user.return_value = User(
        id=uuid4(),
        full_name="New User",
        username="newuser",
        email="newuser@example.com",
        hashed_password="hashedpassword",
        is_verified=False,
        user_type=UserType.REGULAR,
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
    )
    mock_send_email.return_value = None

    payload = {
        "full_name": "New User",
        "username": "newuser",
        "email": "newuser@example.com",
        "hashed_password": "plaintextpassword",
        "accepted_terms": True,
        "accepted_privacy_policy": True,
    }

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()


# Test user login
@patch("backend.api.auth.auth_service.authenticate_user")
@patch("backend.api.auth.auth_routes.create_session")
def test_login_user(mock_create_session, mock_authenticate_user, mock_user, db_session):
    mock_authenticate_user.return_value = mock_user
    mock_create_session.return_value = "session-token-123"

    payload = {
        "email": mock_user.email,
        "password": "plaintextpassword",
    }

    response = client.post("/api/auth/login", json=payload)

    assert response.status_code == 200
    assert response.json()["access_token"] == "session-token-123"


# Test verifying email
@patch("backend.api.auth.auth_routes.jwt.decode")
def test_verify_email(mock_jwt_decode, mock_user, db_session):
    mock_jwt_decode.return_value = {"sub": str(mock_user.id), "type": "email_verification"}

    response = client.get("/api/auth/verify-email?token=fake-token")

    assert response.status_code == 200
    assert "status" in response.json()
    assert "success" in response.json()


# Test resending verification email
@patch("backend.api.auth.auth_routes.send_email")
def test_resend_verification_email(mock_send_email, mock_user, db_session):
    mock_send_email.return_value = None

    with patch("backend.api.auth.auth_routes.get_current_user", return_value=mock_user):
        response = client.post("/api/auth/resend-verification")
        assert response.status_code == 200
        assert response.json()["message"] == "Verification email resent successfully."


# Test logging out
@patch("backend.api.auth.auth_routes.invalidate_specific_session")
def test_logout_user(mock_invalidate_specific_session, mock_user, db_session):
    mock_invalidate_specific_session.return_value = None

    with patch("backend.api.auth.auth_routes.get_current_user", return_value=mock_user):
        response = client.post("/api/auth/logout")
        assert response.status_code == 200
        assert response.json()["message"] == "Logged out successfully."


# Test logging out all sessions
@patch("backend.api.auth.auth_routes.invalidate_session")
def test_logout_all_sessions(mock_invalidate_session, mock_user, db_session):
    mock_invalidate_session.return_value = None

    with patch("backend.api.auth.auth_routes.get_current_user", return_value=mock_user):
        response = client.post("/api/auth/logout-all")
        assert response.status_code == 200
        assert response.json()["message"] == "All sessions logged out successfully."
