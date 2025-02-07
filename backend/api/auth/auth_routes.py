from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import HTTPBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from urllib.parse import urlencode
from uuid import UUID

from backend.core.database import get_db
from backend.api.auth.auth_service import (
    create_user, get_user_by_username, get_user_by_email, verify_password,
    get_current_user
)
from backend.schemas.user_schema import UserCreate, Token, LoginRequest
from backend.core.config import settings
from backend.services.session_service import create_session, validate_session, deactivate_session, deactivate_specific_session
from backend.models.user import User, SetupStep
from backend.core.logging_config import get_logger
from backend.templates.email_templates import EMAIL_VERIFICATION_TEMPLATE
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

auth_scheme = HTTPBearer()
logger = get_logger(__name__)
router = APIRouter()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
EMAIL_TOKEN_EXPIRE_MINUTES = 60
email_cooldown_cache = {}

async def send_email(subject: str, recipient: str, template, context: dict):
    """ Sends an email using FastMail and the provided Jinja2 template. """
    try:
        body = template.render(context)
        message = MessageSchema(subject=subject, recipients=[recipient], body=body, subtype="html")
        fm = FastMail(ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=settings.USE_CREDENTIALS,
        ))
        await fm.send_message(message)
        logger.info(f"Email sent to {recipient}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")

@router.post("/register", response_model=Token)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """ Registers a new user and sends an email verification link. """
    if not user.accepted_privacy_policy or not user.accepted_terms:
        raise HTTPException(status_code=400, detail="You must accept terms and privacy policy")

    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user)
    new_user.setup_step = SetupStep.email_verification
    new_user.profile_version = 1
    db.commit()

    token_data = {"sub": str(new_user.id), "type": "email_verification"}
    verification_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    verification_link = f"{settings.BASE_URL}/api/auth/verify-email?token={verification_token}"

    context = {"username": user.username, "verification_link": verification_link, "current_year": datetime.now().year}
    await send_email("Verify Your Email", user.email, EMAIL_VERIFICATION_TEMPLATE, context)

    session_token = create_session(new_user.id, db)
    return {"access_token": session_token, "token_type": "bearer", "status": "pending"}

@router.get("/verify-email", include_in_schema=False)
async def verify_email(token: str, db: Session = Depends(get_db)):
    """ Verifies a user's email address. """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = UUID(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            return RedirectResponse(url=f"{settings.FRONTEND_URL}/verify-email?{urlencode({'status': 'already_verified'})}")

        user.is_verified = True
        user.setup_step = SetupStep.profile_completion
        user.profile_version += 1
        db.commit()

        session_token = create_session(user.id, db)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/verify-email?{urlencode({'status': 'success', 'token': session_token})}")

    except ExpiredSignatureError:
        logger.warning("Verification link expired")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/verify-email?{urlencode({'status': 'expired'})}")
    except JWTError:
        logger.error("Invalid verification token")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/verify-email?{urlencode({'status': 'invalid'})}")
    except Exception as e:
        logger.exception("Error during email verification")
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/verify-email?{urlencode({'status': 'error'})}")

@router.post("/login", response_model=Token)
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    """ Handles user login and creates a session with device details. """
    logger.info(f"Login attempt for email: {login_data.email}, is_mobile: {login_data.is_mobile}")

    user = get_user_by_email(db, login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")

    # Extract device details
    user_agent = request.headers.get("User-Agent", "Unknown")
    ip_address = request.client.host

    token = create_session(
        user.id, db, login_data.is_mobile,
        device_type="Mobile" if login_data.is_mobile else "Desktop",
        device_os=user_agent,
        browser="Unknown",  # Can be parsed from user_agent
        location="Unknown",  # Could be implemented with IP tracking
        ip_address=ip_address
    )

    logger.info(f"Session created for user: {user.email}")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/resend-verification")
async def resend_verification_email(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """ Resends a verification email if allowed by the cooldown system. """
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
    verification_link = f"{settings.BASE_URL}/api/auth/verify-email?token={verification_token}"

    context = {
        "username": current_user.username,
        "verification_link": verification_link,
        "current_year": datetime.now().year,
    }

    await send_email("Verify Your Email", current_user.email, EMAIL_VERIFICATION_TEMPLATE, context)
    email_cooldown_cache[user_id] = now
    return {"message": "Verification email resent successfully"}

@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    token: str = Depends(auth_scheme),
):
    """ Logs out a user by deactivating the session. """
    deactivate_specific_session(token.credentials, db)
    return {"message": "Logged out successfully"}

@router.post("/logout-all")
def logout_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """ Logs out all sessions for a user by deactivating them. """
    deactivate_session(current_user.id, db)
    return {"message": "All sessions logged out successfully"}
