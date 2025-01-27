import pytest
from uuid import uuid4
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import datetime
from backend.api.admin.admin_routes import router
from backend.core.config import settings
from backend.main import app
from backend.models.user import User, UserType

# Add the router to the test app
app.include_router(router)
client = TestClient(app)


# Fixture to create a mock admin user
@pytest.fixture
def mock_admin_user(db_session):
    user = User(
        id=uuid4(),
        full_name="Admin User",
        username="adminuser",
        email="admin@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        is_verified=True,
        user_type=UserType.ADMIN,
        admin_secret_key=settings.SUPERUSER_CREATION_SECRET_KEY,
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
    )
    db_session.add(user)
    db_session.commit()
    return user


# Test creating an admin user
@patch("backend.api.admin.admin_service.create_admin_user")
def test_create_admin_user(mock_create_admin_user, db_session):
    mock_create_admin_user.return_value = User(
        id=uuid4(),
        full_name="New Admin",
        username="newadmin",
        email="newadmin@example.com",
        user_type=UserType.ADMIN,
        is_active=True,
        is_verified=True,
    )

    payload = {
        "full_name": "New Admin",
        "username": "newadmin",
        "email": "newadmin@example.com",
        "hashed_password": "plaintextpassword",
        "accepted_terms": True,
        "accepted_privacy_policy": True,
        "admin_secret_key": settings.SUPERUSER_CREATION_SECRET_KEY,
    }

    headers = {"x-superuser-secret": settings.SUPERUSER_CREATION_SECRET_KEY}
    response = client.post("/api/admin/create", json=payload, headers=headers)
    assert response.status_code == 200
    assert "Admin user newadmin created successfully" in response.json()["message"]


# Test admin login
@patch("backend.api.admin.admin_routes.create_session")
def test_admin_login(mock_create_session, mock_admin_user, db_session):
    mock_create_session.return_value = "session-token-123"

    payload = {"email": mock_admin_user.email, "password": "plaintextpassword"}

    with patch("backend.api.auth.auth_service.verify_password", return_value=True):
        response = client.post("/api/admin/login", json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["session_token"] == "session-token-123"


# Test generating MFA setup
@patch("backend.api.admin.admin_routes.generate_mfa_secret")
def test_get_mfa_setup(mock_generate_mfa_secret, mock_admin_user, db_session):
    mock_generate_mfa_secret.return_value = {
        "qr_code": "test-qr-code",
        "manual_key": "manual-key-123",
    }

    headers = {"x-superuser-secret": settings.SUPERUSER_CREATION_SECRET_KEY}
    response = client.get(f"/api/admin/mfa/setup?user_id={mock_admin_user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["qr_code_url"] == "test-qr-code"
    assert response.json()["manual_key"] == "manual-key-123"


# Test verifying MFA
@patch("backend.api.admin.admin_routes.verify_mfa_code")
def test_post_mfa_verify(mock_verify_mfa_code, mock_admin_user, db_session):
    mock_verify_mfa_code.return_value = True

    payload = {
        "user_id": str(mock_admin_user.id),
        "totp_code": "123456",
        "session_token": "test-session-token",
    }

    headers = {"x-superuser-secret": settings.SUPERUSER_CREATION_SECRET_KEY}
    response = client.post("/api/admin/mfa/verify", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "MFA verification successful"


# Test listing admin users
@patch("backend.api.admin.admin_service.list_admin_users")
def test_list_admins(mock_list_admin_users, mock_admin_user, db_session):
    mock_list_admin_users.return_value = [mock_admin_user]

    headers = {"x-superuser-secret": settings.SUPERUSER_CREATION_SECRET_KEY}
    response = client.get("/api/admin/list", headers=headers)
    assert response.status_code == 200
    admins = response.json()
    assert len(admins) == 1
    assert admins[0]["username"] == mock_admin_user.username


# Test moderating flagged users
@patch("backend.api.admin.admin_service.moderate_flagged_users")
def test_moderate_flagged_users(mock_moderate_flagged_users, db_session):
    mock_moderate_flagged_users.return_value = [
        {"id": "user-id-123", "username": "flaggeduser", "flagged_for_review": True}
    ]

    headers = {"x-superuser-secret": settings.SUPERUSER_CREATION_SECRET_KEY}
    response = client.get("/api/admin/moderate-flagged", headers=headers)
    assert response.status_code == 200
    flagged_users = response.json()
    assert len(flagged_users) == 1
    assert flagged_users[0]["username"] == "flaggeduser"
