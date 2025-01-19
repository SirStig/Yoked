from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.logging_config import get_logger
from backend.models.user import User
from backend.models.session import Session as SessionModel
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
    - data: Dictionary of claims.
    - expires_delta: Optional expiration time override.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a user by username.
    - db: Database session.
    - username: Username to look up.
    """
    user = db.query(User).filter(User.username == username).first()
    return user

def get_user_by_email(db: Session, email: str) -> User:
    """
    Fetch a user by their email address.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.
    - db: Database session.
    - user: UserCreate schema instance.
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
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(username: str, password: str, db: Session) -> User:
    """
    Authenticate the user by username and password.
    - username: Username provided by the user.
    - password: Password provided by the user.
    - db: Database session.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    return user


def login_user(username: str, password: str, db: Session, is_mobile: bool = False) -> str:
    """
    Log in a user by creating a new session token.
    - username: Username of the user.
    - password: Password of the user.
    - db: Database session.
    - is_mobile: Indicates if the session is for a mobile device.
    """
    user = authenticate_user(username, password, db)
    token = create_session(user.id, db, is_mobile)
    return token


from fastapi import Header


def get_current_user(
        token: str = Header(..., alias="Authorization"), db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user based on the session token.
    - token: Session token from the Authorization header.
    - db: Database session.
    """
    logger.debug(f"Authorization header token: {token}")
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    else:
        logger.error("Invalid Authorization header format")
        raise HTTPException(status_code=401, detail="Invalid token format")

    session = validate_session(token, db)
    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        logger.error(f"User not found for session user_id: {session.user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.debug(f"User retrieved: {user.__dict__}")
    return user


def logout_user(token: str, db: Session):
    """
    Log out the user by invalidating the current session.
    - token: Session token.
    - db: Database session.
    """
    invalidate_specific_session(token, db)


def logout_all_sessions(user_id: int, db: Session):
    """
    Log out the user by invalidating all their sessions.
    - user_id: ID of the user.
    - db: Database session.
    """
    invalidate_session(user_id, db)
