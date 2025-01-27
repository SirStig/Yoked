import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from datetime import datetime
from backend.api.auth.auth_service import (
    create_user,
    authenticate_user,
    verify_password,
    hash_password,
    create_access_token,
    get_user_by_username,
)
from backend.schemas.user_schema import UserCreate
from backend.models.user import UserType


# Fixture to create a mock user payload
@pytest.fixture
def mock_user_payload():
    return UserCreate(
        full_name="Test User",
        username="testuser",
        email="testuser@example.com",
        hashed_password="plaintextpassword",
        accepted_terms=True,
        accepted_privacy_policy=True,
        user_type=UserType.REGULAR,  # Ensure enum matches the model
    )


# Test user creation
def test_create_user(db_session: Session, mock_user_payload):
    user = create_user(db_session, mock_user_payload)

    assert user.username == mock_user_payload.username
    assert user.email == mock_user_payload.email
    assert user.full_name == mock_user_payload.full_name
    assert user.user_type == UserType.REGULAR  # Verify correct enum
    assert user.is_active is True
    assert user.is_verified is False
    assert user.accepted_terms is True
    assert user.accepted_privacy_policy is True
    assert user.accepted_terms_at is not None
    assert user.accepted_privacy_policy_at is not None


# Test password hashing and verification
def test_password_hashing():
    plain_password = "plaintextpassword"
    hashed_password = hash_password(plain_password)

    assert verify_password(plain_password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


# Test token creation
def test_create_access_token():
    data = {"sub": "user_id_123"}
    token = create_access_token(data=data)

    assert token is not None
    assert isinstance(token, str)


# Test authenticating a user
def test_authenticate_user(db_session: Session, mock_user_payload):
    created_user = create_user(db_session, mock_user_payload)

    # Attempt authentication
    authenticated_user = authenticate_user(
        username=created_user.username,
        password=mock_user_payload.hashed_password,
        db=db_session,
    )

    assert authenticated_user is not None
    assert authenticated_user.username == created_user.username
    assert authenticated_user.is_active is True
    assert authenticated_user.accepted_terms is True
    assert authenticated_user.accepted_privacy_policy is True


# Test fetching a user by username
def test_get_user_by_username(db_session: Session, mock_user_payload):
    created_user = create_user(db_session, mock_user_payload)

    fetched_user = get_user_by_username(db_session, created_user.username)

    assert fetched_user is not None
    assert fetched_user.username == created_user.username
    assert fetched_user.email == created_user.email
    assert fetched_user.full_name == created_user.full_name


# Test authentication failure with invalid username
def test_authenticate_user_invalid_username(db_session: Session, mock_user_payload):
    create_user(db_session, mock_user_payload)

    with pytest.raises(Exception) as exc_info:
        authenticate_user(username="invaliduser", password="plaintextpassword", db=db_session)

    assert "Invalid username or password" in str(exc_info.value)


# Test authentication failure with incorrect password
def test_authenticate_user_invalid_password(db_session: Session, mock_user_payload):
    create_user(db_session, mock_user_payload)

    with pytest.raises(Exception) as exc_info:
        authenticate_user(username=mock_user_payload.username, password="wrongpassword", db=db_session)

    assert "Invalid username or password" in str(exc_info.value)
