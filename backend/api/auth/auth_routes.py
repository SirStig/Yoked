from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import jwt
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.auth.auth_service import (
    create_user,
    get_user_by_username,
    hash_password,
    get_current_user,
    verify_password, get_user_by_email,
)
from backend.schemas.user_schema import UserCreate, Token, LoginRequest
from backend.core.config import settings
from backend.services.session_service import (
    create_session,
    validate_session,
    invalidate_session,
    invalidate_specific_session,
)
from backend.models.user import User, SetupStep  # Importing User model
from backend.core.logging_config import get_logger
from uuid import UUID  # Ensure proper handling of UUIDs

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter()

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
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
)

# Base URL for dynamic link generation
BASE_URL = settings.BASE_URL
FRONTEND_BASE_URL = settings.FRONTEND_URL


# Helper function to send emails
async def send_email(subject: str, recipient: str, body: str):
    logger.debug("Preparing to send email")
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype="html",
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"Email sent to {recipient}")
    except Exception as e:
        logger.exception(f"Failed to send email to {recipient}: {e}")
        raise HTTPException(status_code=500, detail="Email sending failed")


# Route: Register user with email verification
@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if not user.accepted_privacy_policy or not user.accepted_terms:
        raise HTTPException(status_code=400, detail="User must accept terms and conditions")

    try:
        existing_user = get_user_by_username(db, user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        new_user = create_user(db, user)
        new_user.setup_step = SetupStep.email_verification

        token_data = {"sub": str(new_user.id), "type": "email_verification"}

        verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        session_token = create_session(new_user.id, db)

        verification_link = f"{settings.BASE_URL}/api/auth/verify-email?token={verification_token}"
        email_body = f"Click the link to verify your email: <a href='{verification_link}'>{verification_link}</a>"
        await send_email("Verify Your Email", user.email, email_body)

        return {"access_token": session_token, "token_type": "bearer", "status": "pending"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")


# Route: Login
@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Handles user login by verifying credentials and creating a session.
    """
    logger.info(f"Login attempt for email: {request.email}, is_mobile: {request.is_mobile}")  # Adjust logging for clarity

    # Fetch user by email
    user = get_user_by_email(db, request.email)

    if not user:
        logger.warning(f"User with email {request.email} not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Log and verify password
    logger.debug(f"Stored hashed password for user {user.email}: {user.hashed_password}")

    if not verify_password(request.password, user.hashed_password):
        logger.warning(f"Password verification failed for email {user.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        logger.warning(f"Inactive user {user.email} attempted login")
        raise HTTPException(status_code=403, detail="User account is inactive")

    # Create a session
    token = create_session(user.id, db, request.is_mobile)
    logger.info(f"Session created for email: {user.email}")
    return {"access_token": token, "token_type": "bearer"}



# Route: Verify email using token
@router.get("/verify-email", include_in_schema=False)
async def verify_email(token: str, db: Session = Depends(get_db)):
    logger.info("Processing email verification")
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded token payload: {payload}")

        # Validate the token type
        if payload.get("type") != "email_verification":
            logger.warning("Invalid token type for email verification")
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = UUID(payload.get("sub"))  # Decode user_id as UUID
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User {user_id} not found for email verification")
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            logger.info(f"User {user_id} already verified")
            return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?status=already_verified")

        # Update user to mark as verified and move to the next setup step
        user.is_verified = True
        user.setup_step = SetupStep.profile_completion
        db.commit()

        logger.info(f"Email verified for user {user_id}")

        # Create a session after successful email verification
        session_token = create_session(user.id, db)
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?status=success")

    except jwt.ExpiredSignatureError:
        logger.exception("Token verification failed: Token expired")
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?status=expired")
    except jwt.JWTError:
        logger.exception("Token verification failed: JWT error")
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?status=invalid")
    except Exception as e:
        logger.exception("Unexpected error during email verification")
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?status=error")

email_cooldown_cache = {}  # {user_id: datetime}

@router.post("/resend-verification")
async def resend_verification_email(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    now = datetime.utcnow()

    # Check cooldown
    if user_id in email_cooldown_cache:
        last_sent_time = email_cooldown_cache[user_id]
        cooldown_remaining = (last_sent_time + timedelta(seconds=30)) - now
        if cooldown_remaining > timedelta(0):
            logger.warning(f"User {user_id} attempted to resend email within cooldown period")
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {int(cooldown_remaining.total_seconds())} seconds before resending the email."
            )

    # Refresh the verification token
    token_data = {"sub": str(user_id), "type": "email_verification"}
    verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    verification_link = f"{BASE_URL}/api/auth/verify-email?token={verification_token}"

    email_body = f"Click the link to verify your email: <a href='{verification_link}'>{verification_link}</a>"

    try:
        await send_email("Verify Your Email", current_user.email, email_body)
        logger.info(f"Verification email resent to user {user_id}")
        email_cooldown_cache[user_id] = now
        return {"message": "Verification email resent successfully"}
    except Exception as e:
        logger.exception(f"Failed to resend email verification to user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to resend verification email")

# Route: Logout (invalidate a session)
@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Logout attempt by user ID: {current_user.id}")
    invalidate_specific_session(current_user.id, db)
    logger.info(f"Session invalidated for user ID: {current_user.id}")
    return {"message": "Logged out successfully"}


# Route: Logout all sessions
@router.post("/logout-all")
def logout_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Logout all sessions request for user ID: {current_user.id}")
    invalidate_session(current_user.id, db)
    logger.info(f"All sessions invalidated for user ID: {current_user.id}")
    return {"message": "All sessions logged out successfully"}
