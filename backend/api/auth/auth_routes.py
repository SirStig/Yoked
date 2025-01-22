from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from urllib.parse import urlencode
from backend.core.database import get_db
from backend.api.auth.auth_service import (
    create_user, get_user_by_username, get_user_by_email, verify_password,
    hash_password, get_current_user,
)
from backend.schemas.user_schema import UserCreate, Token, LoginRequest
from backend.core.config import settings
from backend.services.session_service import create_session, validate_session, invalidate_session, invalidate_specific_session
from backend.models.user import User, SetupStep
from backend.core.logging_config import get_logger
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from uuid import UUID

auth_scheme = HTTPBearer()
logger = get_logger(__name__)
router = APIRouter()

# JWT and Email Configurations
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
EMAIL_TOKEN_EXPIRE_MINUTES = 60
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
BASE_URL = settings.BASE_URL
FRONTEND_BASE_URL = settings.FRONTEND_URL
email_cooldown_cache = {}

# Helper Function to Send Emails
async def send_email(subject: str, recipient: str, body: str):
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
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")


# Route: Register user with email verification
@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if not user.accepted_privacy_policy or not user.accepted_terms:
        raise HTTPException(status_code=400, detail="You must accept terms and privacy policy")

    try:
        # Check for existing username or email
        if get_user_by_username(db, user.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = create_user(db, user)
        new_user.setup_step = SetupStep.email_verification
        new_user.profile_version = 1
        db.commit()

        # Generate and send verification email
        token_data = {"sub": str(new_user.id), "type": "email_verification"}
        verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        verification_link = f"{BASE_URL}/api/auth/verify-email?token={verification_token}"
        await send_email("Verify Your Email", user.email, f"Click here to verify: {verification_link}")

        # Create a session
        session_token = create_session(new_user.id, db)
        return {"access_token": session_token, "token_type": "bearer", "status": "pending"}

    except HTTPException as e:
        logger.error(f"Registration failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during registration")
        raise HTTPException(status_code=500, detail="Registration failed")


# Route: Verify email using token
@router.get("/verify-email", include_in_schema=False)
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = UUID(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?{urlencode({'status': 'already_verified'})}")

        user.is_verified = True
        user.setup_step = SetupStep.profile_completion
        user.profile_version += 1
        db.commit()

        session_token = create_session(user.id, db)
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?{urlencode({'status': 'success', 'token': session_token})}")

    except ExpiredSignatureError:
        logger.warning("Verification link expired")
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?{urlencode({'status': 'expired'})}")
    except JWTError:
        logger.error("Invalid verification token")
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?{urlencode({'status': 'invalid'})}")
    except Exception as e:
        logger.exception("Error during email verification")
        return RedirectResponse(url=f"{FRONTEND_BASE_URL}/verify-email?{urlencode({'status': 'error'})}")


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Handles user login by verifying credentials and creating a session.
    """
    logger.info(f"Login attempt for email: {request.email}, is_mobile: {request.is_mobile}")

    # Fetch user by email
    user = get_user_by_email(db, request.email)

    if not user:
        logger.warning(f"User with email {request.email} not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

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

# Route: Resend verification email
@router.post("/resend-verification")
async def resend_verification_email(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id = current_user.id
    now = datetime.utcnow()

    if user_id in email_cooldown_cache:
        last_sent_time = email_cooldown_cache[user_id]
        cooldown_remaining = (last_sent_time + timedelta(seconds=30)) - now
        if cooldown_remaining > timedelta(0):
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {int(cooldown_remaining.total_seconds())} seconds before resending the email."
            )

    token_data = {"sub": str(user_id), "type": "email_verification"}
    verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    verification_link = f"{BASE_URL}/api/auth/verify-email?token={verification_token}"

    email_body = f"Click the link to verify your email: <a href='{verification_link}'>{verification_link}</a>"
    await send_email("Verify Your Email", current_user.email, email_body)
    email_cooldown_cache[user_id] = now
    return {"message": "Verification email resent successfully"}


# Route: Logout
@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(auth_scheme),
):
    invalidate_specific_session(token.credentials, db)
    return {"message": "Logged out successfully"}


# Route: Logout all sessions
@router.post("/logout-all")
def logout_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    invalidate_session(current_user.id, db)
    return {"message": "All sessions logged out successfully"}
