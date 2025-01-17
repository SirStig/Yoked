from fastapi import APIRouter, HTTPException, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from backend.core.database import get_db
from backend.api.auth.auth_service import create_user, get_user_by_username, hash_password, verify_password
from backend.schemas.user_schema import UserCreate, Token
from backend.core.config import settings
from backend.core.aws_utils import upload_file_to_s3
from backend.models.user import User
from pydantic import BaseModel, EmailStr
import logging

from backend.services.session_service import create_session

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
EMAIL_TOKEN_EXPIRE_MINUTES = 60

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS
)

# Base URL for dynamic link generation
BASE_URL = settings.BASE_URL

router = APIRouter()

# Helper function to send emails
async def send_email(subject: str, recipient: str, body: str):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email sent to {recipient}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        raise HTTPException(status_code=500, detail="Email sending failed")

# Route: Register user with email verification
@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        logger.warning(f"Registration attempt with existing username: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = create_user(db, user)
    token_data = {"sub": new_user.username, "type": "email_verification"}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    verification_link = f"{BASE_URL}/api/auth/verify-email?token={token}"
    email_body = f"Click the link to verify your email: <a href='{verification_link}'>{verification_link}</a>"

    await send_email("Verify Your Email", user.email, email_body)
    logger.info(f"Verification email sent to {user.email}")

    return {"access_token": token, "token_type": "bearer"}

# Route: Verify email
@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "email_verification":
            logger.warning(f"Invalid token type for email verification")
            raise HTTPException(status_code=400, detail="Invalid token type")

        username = payload.get("sub")
        user = get_user_by_username(db, username)
        if not user:
            logger.error(f"Email verification failed: User {username} not found")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Email verified for user {username}")
        return {"message": "Email verified successfully"}
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid or expired token")

# Route: Password reset request
@router.post("/password-reset")
async def password_reset_request(email: EmailStr, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"Password reset requested for non-existent email: {email}")
        raise HTTPException(status_code=404, detail="User not found")

    token_data = {"sub": user.username, "type": "password_reset"}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    reset_link = f"{BASE_URL}/api/auth/reset-password?token={token}"
    email_body = f"Click the link to reset your password: <a href='{reset_link}'>{reset_link}</a>"

    await send_email("Password Reset", email, email_body)
    logger.info(f"Password reset email sent to {email}")

    return {"message": "Password reset email sent"}

# Route: Reset password
@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "password_reset":
            logger.warning(f"Invalid token type for password reset")
            raise HTTPException(status_code=400, detail="Invalid token type")

        username = payload.get("sub")
        user = get_user_by_username(db, username)
        if not user:
            logger.error(f"Password reset failed: User {username} not found")
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = hash_password(new_password)
        db.commit()
        logger.info(f"Password reset for user {username}")

        return {"message": "Password reset successfully"}
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid or expired token")


@router.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_session(user.id, db)
    return {"access_token": token, "token_type": "bearer"}