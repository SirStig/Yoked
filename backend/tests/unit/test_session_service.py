import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from uuid import uuid4
from backend.services.session_service import (
    create_session,
    validate_session,
    invalidate_session,
    invalidate_specific_session,
    get_active_sessions,
    fetch_user_sessions,
)
from backend.models.session import SessionModel
from backend.models.user import User, UserType
from backend.schemas.session_schema import UserSession


# Fixture for creating a mock user
@pytest.fixture
def mock_user(db_session: Session):
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


# Test creating a session
def test_create_session(db_session: Session, mock_user):
    session = create_session(
        user_id=mock_user.id,
        db=db_session,
        is_mobile=False,
        device_type="Desktop",
        location="USA",
        ip_address="192.168.1.1",
    )

    assert session is not None
    assert session.user_id == mock_user.id
    assert session.is_mobile is False
    assert session.device_type == "Desktop"
    assert session.location == "USA"
    assert session.ip_address == "192.168.1.1"


# Test validating a session
def test_validate_session(db_session: Session, mock_user):
    session = create_session(
        user_id=mock_user.id,
        db=db_session,
        is_mobile=False,
        device_type="Desktop",
    )

    validated_session = validate_session(session.token, db_session)

    assert validated_session is not None
    assert validated_session.token == session.token
    assert validated_session.user_id == mock_user.id


# Test invalidating a specific session
def test_invalidate_specific_session(db_session: Session, mock_user):
    session = create_session(user_id=mock_user.id, db=db_session, is_mobile=False)

    invalidate_specific_session(session.token, db_session)

    invalidated_session = db_session.query(SessionModel).filter(SessionModel.token == session.token).first()
    assert invalidated_session is None


# Test invalidating all sessions
def test_invalidate_all_sessions(db_session: Session, mock_user):
    create_session(user_id=mock_user.id, db=db_session, is_mobile=False)
    create_session(user_id=mock_user.id, db=db_session, is_mobile=True)

    invalidate_session(user_id=mock_user.id, db=db_session)

    active_sessions = db_session.query(SessionModel).filter(SessionModel.user_id == mock_user.id).all()
    assert len(active_sessions) == 0


# Test fetching active sessions
def test_get_active_sessions(db_session: Session, mock_user):
    create_session(user_id=mock_user.id, db=db_session, is_mobile=False, device_type="Desktop", location="USA", ip_address="192.168.1.1")
    create_session(user_id=mock_user.id, db=db_session, is_mobile=True, device_type="Mobile", location="Canada", ip_address="192.168.1.2")

    sessions = get_active_sessions(user_id=mock_user.id, db=db_session)

    assert len(sessions) == 2
    assert all(isinstance(session, UserSession) for session in sessions)
    assert all(session.user_id == mock_user.id for session in sessions)
    assert {s.device_type for s in sessions} == {"Desktop", "Mobile"}
    assert {s.location for s in sessions} == {"USA", "Canada"}


# Test fetching user sessions with detailed output
def test_fetch_user_sessions(db_session: Session, mock_user):
    create_session(user_id=mock_user.id, db=db_session, is_mobile=False, device_type="Desktop", location="USA", ip_address="192.168.1.1")
    create_session(user_id=mock_user.id, db=db_session, is_mobile=True, device_type="Mobile", location="Canada", ip_address="192.168.1.2")

    sessions = fetch_user_sessions(user_id=mock_user.id, db=db_session)

    assert len(sessions) == 2
    for session in sessions:
        assert isinstance(session, UserSession)
        assert session.user_id == mock_user.id
        assert session.device_type in ["Desktop", "Mobile"]
        assert session.location in ["USA", "Canada"]
