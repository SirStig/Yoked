from uuid import uuid4
import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from datetime import datetime
from backend.services.mfa import generate_mfa_secret, verify_mfa_code, reset_mfa
from backend.models.user import User, UserType
from fastapi import HTTPException


# Fixture to create a mock user
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
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
        mfa_secret="dummy_secret",
        mfa_backup_codes=["code1", "code2"],
        mfa_enabled=True,
    )
    db_session.add(user)
    db_session.commit()
    return user


# Test generating MFA secret
def test_generate_mfa_secret():
    mfa_data = generate_mfa_secret(email="testuser@example.com")

    assert "mfa_secret" in mfa_data
    assert "qr_code" in mfa_data
    assert "manual_key" in mfa_data
    assert mfa_data["mfa_secret"] == mfa_data["manual_key"]


# Test verifying a correct MFA code
@patch("pyotp.TOTP.verify", return_value=True)
def test_verify_mfa_code_success(mock_verify):
    secret = "dummy_secret"
    code = "123456"

    result = verify_mfa_code(secret, code)
    assert result is True


# Test verifying an incorrect MFA code
@patch("pyotp.TOTP.verify", return_value=False)
def test_verify_mfa_code_failure(mock_verify):
    secret = "dummy_secret"
    code = "wrong_code"

    result = verify_mfa_code(secret, code)
    assert result is False


# Test resetting MFA
def test_reset_mfa(mock_user, db_session):
    reset_mfa(mock_user.id, db_session)

    user = db_session.query(User).filter(User.id == mock_user.id).first()
    assert user.mfa_secret is None
    assert user.mfa_backup_codes is None
    assert user.mfa_enabled is False


# Test resetting MFA for a non-existent user
def test_reset_mfa_user_not_found(db_session):
    non_existent_user_id = uuid4()  # Generate a non-existent UUID
    with pytest.raises(HTTPException) as excinfo:
        reset_mfa(non_existent_user_id, db_session)

    assert excinfo.value.status_code == 404
    assert "User not found" in str(excinfo.value)
