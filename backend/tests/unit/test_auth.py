import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.models.user import User
from sqlalchemy.orm import Session
from jose import jwt
from backend.core.config import settings

client = TestClient(app)

def create_test_user(db: Session, username: str, email: str, full_name: str = "Test User", is_verified: bool = False):
    user = User(
        full_name=full_name,
        username=username,
        email=email,
        hashed_password="hashedpassword",
        is_verified=is_verified,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def generate_token(username: str, token_type: str):
    payload = {"sub": username, "type": token_type}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def test_verify_email_valid_token(db_session):
    username = "testuser"
    email = "testuser@example.com"
    create_test_user(db_session, username, email)
    token = generate_token(username, "email_verification")

    response = client.get(f"/api/auth/verify-email?token={token}")
    assert response.status_code == 200
    assert response.json() == {"message": "Email verified successfully"}

def test_verify_email_already_verified(db_session):
    username = "verifieduser"
    email = "verifieduser@example.com"
    create_test_user(db_session, username, email, is_verified=True)
    token = generate_token(username, "email_verification")

    response = client.get(f"/api/auth/verify-email?token={token}")
    assert response.status_code == 200
    assert response.json() == {"message": "Email already verified"}

def test_verify_email_nonexistent_user(db_session):
    token = generate_token("nonexistentuser", "email_verification")

    response = client.get(f"/api/auth/verify-email?token={token}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
