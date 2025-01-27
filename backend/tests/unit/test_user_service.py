import pytest
from sqlalchemy.orm import Session
from datetime import datetime
from unittest.mock import patch
from backend.api.auth.auth_service import create_user, authenticate_user, get_user_by_username
from backend.schemas.user_schema import UserCreate
from backend.models.user import UserType


# Helper fixture for creating a mock user creation payload
@pytest.fixture
def user_create_payload():
    return UserCreate(
        full_name="Test User",
        username="testuser",
        email="testuser@example.com",
        hashed_password="plaintextpassword",
        accepted_terms=True,
        accepted_privacy_policy=True,
        user_type=UserType.REGULAR,  # Ensure enum matches the model
    )


# Test creating a user
def test_create_user(db_session: Session, user_create_payload):
    user = create_user(db_session, user_create_payload)

    assert user.username == user_create_payload.username
    assert user.email == user_create_payload.email
    assert user.full_name == user_create_payload.full_name
    assert user.user_type == UserType.REGULAR  # Verify correct enum
    assert user.is_active is True
    assert user.is_verified is False
    assert user.accepted_terms is True
    assert user.accepted_privacy_policy is True
    assert user.accepted_terms_at is not None
    assert user.accepted_privacy_policy_at is not None


# Test fetching user by username
def test_get_user_by_username(db_session: Session, user_create_payload):
    created_user = create_user(db_session, user_create_payload)

    fetched_user = get_user_by_username(db_session, created_user.username)

    assert fetched_user is not None
    assert fetched_user.username == created_user.username
    assert fetched_user.email == created_user.email
    assert fetched_user.full_name == created_user.full_name


# Test authenticating a user
def test_authenticate_user(db_session: Session, user_create_payload):
    created_user = create_user(db_session, user_create_payload)

    # Simulate verified email for successful login
    created_user.is_verified = True
    db_session.commit()

    # Attempt authentication
    authenticated_user = authenticate_user(
        username=created_user.username,
        password=user_create_payload.hashed_password,
        db=db_session,
    )

    assert authenticated_user is not None
    assert authenticated_user.username == created_user.username
    assert authenticated_user.email == created_user.email
    assert authenticated_user.is_active is True
    assert authenticated_user.accepted_terms is True
    assert authenticated_user.accepted_privacy_policy is True


# Test authentication failure with unverified email
def test_authenticate_user_unverified_email(db_session: Session, user_create_payload):
    create_user(db_session, user_create_payload)

    with pytest.raises(Exception) as exc_info:
        authenticate_user(
            username=user_create_payload.username,
            password=user_create_payload.hashed_password,
            db=db_session,
        )

    assert "Email not verified" in str(exc_info.value)


# Test authentication failure with invalid username
def test_authenticate_user_invalid_username(db_session: Session, user_create_payload):
    create_user(db_session, user_create_payload)

    with pytest.raises(Exception) as exc_info:
        authenticate_user(username="invaliduser", password="plaintextpassword", db=db_session)

    assert "Invalid username or password" in str(exc_info.value)


# Test authentication failure with incorrect password
def test_authenticate_user_invalid_password(db_session: Session, user_create_payload):
    create_user(db_session, user_create_payload)

    with pytest.raises(Exception) as exc_info:
        authenticate_user(username=user_create_payload.username, password="wrongpassword", db=db_session)

    assert "Invalid username or password" in str(exc_info.value)
