import pytest
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from backend.api.admin.admin_service import create_admin_user, list_admin_users, moderate_flagged_users
from backend.schemas.user_schema import UserCreate
from backend.models.user import User, UserType

# Fixture for creating a mock admin user payload
@pytest.fixture
def admin_create_payload():
    return UserCreate(
        full_name="Admin User",
        username="adminuser",
        email="admin@example.com",
        hashed_password="hashedpassword",
        accepted_terms=True,
        accepted_privacy_policy=True,
        admin_secret_key="test_secret_key",
        user_type=UserType.ADMIN,
    )

# Test admin user creation
def test_create_admin_user(db_session: Session, admin_create_payload):
    admin_user = create_admin_user(db_session, admin_create_payload)

    assert admin_user.username == admin_create_payload.username
    assert admin_user.email == admin_create_payload.email
    assert admin_user.user_type == UserType.ADMIN
    assert admin_user.is_active is True
    assert admin_user.accepted_terms is True
    assert admin_user.accepted_privacy_policy is True
    assert admin_user.accepted_terms_at is not None
    assert admin_user.accepted_privacy_policy_at is not None

# Test listing admin users
def test_list_admin_users(db_session: Session, admin_create_payload):
    # Create multiple admin users
    create_admin_user(db_session, admin_create_payload)
    admin_create_payload.username = "adminuser2"
    admin_create_payload.email = "admin2@example.com"
    create_admin_user(db_session, admin_create_payload)

    # Fetch all admins
    admins = list_admin_users(db_session)

    assert len(admins) == 2
    assert all(admin.user_type == UserType.ADMIN for admin in admins)

# Test moderating flagged users
def test_moderate_flagged_users(db_session: Session):
    # Create flagged and non-flagged users
    flagged_user = User(
        id=uuid4(),
        full_name="Flagged User",
        username="flagged_user",
        email="flagged@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        user_type=UserType.REGULAR,
        flagged_for_review=True,
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
    )
    non_flagged_user = User(
        id=uuid4(),
        full_name="Normal User",
        username="normal_user",
        email="normal@example.com",
        hashed_password="hashedpassword",
        is_active=True,
        user_type=UserType.REGULAR,
        flagged_for_review=False,
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
    )
    db_session.add(flagged_user)
    db_session.add(non_flagged_user)
    db_session.commit()

    # Fetch flagged users
    flagged_users = moderate_flagged_users(db_session)

    assert len(flagged_users) == 1
    assert flagged_users[0].username == "flagged_user"
    assert flagged_users[0].flagged_for_review is True
