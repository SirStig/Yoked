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
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Temporary tokens for email verification, etc.


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.exception(f"Error verifying password: {e}")
        return False


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a new JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a user by username.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User:
    """
    Fetch a user by their email address.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.
    """
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
        profile_version=1,  # Initialize profile version
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New user created with ID: {new_user.id}, username: {new_user.username}")
    return new_user


def authenticate_user(username: str, password: str, db: Session) -> User:
    """
    Authenticate the user by username and password.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Authentication failed for username: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        logger.warning(f"User {username} attempted login without email verification")
        raise HTTPException(status_code=403, detail="Email not verified")
    logger.info(f"User {username} authenticated successfully")
    return user


def login_user(username: str, password: str, db: Session, is_mobile: bool = False) -> str:
    """
    Log in a user by creating a new session token.
    """
    user = authenticate_user(username, password, db)
    token = create_session(user.id, db, is_mobile)
    logger.info(f"User {username} logged in successfully")
    return token


def get_current_user(
    token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user based on the session token.
    """
    logger.debug(f"Authorization header token: {token}")
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        else:
            raise HTTPException(status_code=401, detail="Invalid token format")

        session = validate_session(token, db)
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user:
            logger.error(f"User not found for session user_id: {session.user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.debug(f"User retrieved: {user.__dict__}")
        return user
    except Exception as e:
        logger.exception(f"Error in retrieving current user: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def admin_required(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify that the current user has admin privileges.
    """
    if not current_user.is_active:
        logger.warning(f"Inactive user attempted admin access. User ID: {current_user.id}")
        raise HTTPException(status_code=403, detail="User account is inactive")
    if not current_user.is_admin:
        logger.warning(f"Non-admin user attempted admin access. User ID: {current_user.id}")
        raise HTTPException(status_code=403, detail="Admin privileges required")
    logger.info(f"Admin access granted for user ID: {current_user.id}")
    return current_user


def logout_user(token: str, db: Session):
    """
    Log out the user by invalidating the current session.
    """
    logger.info("Logging out user")
    invalidate_specific_session(token, db)


def logout_all_sessions(user_id: int, db: Session):
    """
    Log out the user by invalidating all their sessions.
    """
    logger.info(f"Invalidating all sessions for user ID: {user_id}")
    invalidate_session(user_id, db)
