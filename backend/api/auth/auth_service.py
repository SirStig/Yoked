from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Header
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.logging_config import get_logger
from backend.models.user import User
from backend.services.session_service import (
    create_session,
    validate_session,
    invalidate_session,
    invalidate_specific_session,
)
from backend.core.config import settings
from backend.schemas.user_schema import UserCreate

logger = get_logger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.exception("Error hashing password")
        raise HTTPException(status_code=500, detail="Error hashing password")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.exception("Error verifying password")
        return False


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        logger.exception("Error creating access token")
        raise HTTPException(status_code=500, detail="Token generation failed")


def get_user_by_username(db: Session, username: str) -> User:
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
        logger.exception("Error fetching user by username")
        raise HTTPException(status_code=500, detail="Error fetching user by username")


def get_user_by_email(db: Session, email: str) -> User:
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.exception("Error fetching user by email")
        raise HTTPException(status_code=500, detail="Error fetching user by email")


def create_user(db: Session, user: UserCreate) -> User:
    try:
        if get_user_by_username(db, user.username):
            raise HTTPException(status_code=400, detail={"code": "username_exists", "detail": "Username already taken"})
        if get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail={"code": "email_exists", "detail": "Email already registered"})

        hashed_password = hash_password(user.password)
        new_user = User(
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False,
            bio=user.bio,
            profile_picture=user.profile_picture,
            fitness_goals=user.fitness_goals,
            subscription_plan="Free",
            setup_step="email_verification",
            joined_at=datetime.utcnow(),
            accepted_terms=user.accepted_terms,
            accepted_privacy_policy=user.accepted_privacy_policy,
            accepted_terms_at=datetime.utcnow(),
            accepted_privacy_policy_at=datetime.utcnow(),
            profile_version=1,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User created: ID={new_user.id}, username={new_user.username}")
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Error creating user")
        raise HTTPException(status_code=500, detail="User creation failed")


def authenticate_user(username: str, password: str, db: Session) -> User:
    try:
        user = get_user_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed for username: {username}")
            raise HTTPException(
                status_code=401, detail={"code": "invalid_credentials", "detail": "Invalid username or password"}
            )
        if not user.is_verified:
            logger.warning(f"Unverified email login attempt: {username}")
            raise HTTPException(
                status_code=403, detail={"code": "email_not_verified", "detail": "Email not verified"}
            )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Authentication error")
        raise HTTPException(status_code=500, detail="Authentication failed")


def get_current_user(
    token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)
) -> User:
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        else:
            raise HTTPException(status_code=401, detail="Invalid token format")

        session = validate_session(token, db)
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        logger.exception("Invalid JWT token")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        logger.exception("Error fetching current user")
        raise HTTPException(status_code=500, detail="Failed to fetch user")


def admin_required(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


def logout_user(token: str, db: Session):
    try:
        invalidate_specific_session(token, db)
        logger.info("User logged out successfully")
    except Exception as e:
        logger.exception("Error logging out user")
        raise HTTPException(status_code=500, detail="Logout failed")


def logout_all_sessions(user_id: int, db: Session):
    try:
        invalidate_session(user_id, db)
        logger.info(f"All sessions invalidated for user ID: {user_id}")
    except Exception as e:
        logger.exception("Error logging out all sessions")
        raise HTTPException(status_code=500, detail="Logout all sessions failed")
