import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from uuid import UUID
from datetime import datetime

from backend.models import User
from backend.schemas.user_schema import UserCreate, UserType
from backend.services.session_service import create_session
from backend.services.mfa import generate_mfa_secret
from backend.core.logging_config import get_logger

logger = get_logger(__name__)

def hash_password(password: str) -> str:
    """ Securely hashes a password using bcrypt. """
    try:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    except Exception as e:
        logger.exception("Error hashing password")
        raise HTTPException(status_code=500, detail="Password hashing failed")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verifies a password against a stored hash. """
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except Exception as e:
        logger.exception("Error verifying password")
        raise HTTPException(status_code=500, detail="Password verification failed")

def create_user(db: Session, user_data: UserCreate) -> User:
    """ Creates a new user in the database. """
    try:
        logger.info(f"Creating new user: {user_data.username}")

        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")

        hashed_pw = hash_password(user_data.password)

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pw,
            full_name=user_data.full_name,
            bio=user_data.bio,
            profile_picture=user_data.profile_picture,
            fitness_goals=user_data.fitness_goals,
            accepted_terms=user_data.accepted_terms,
            accepted_privacy_policy=user_data.accepted_privacy_policy,
            subscription_plan=user_data.subscription_plan,
            setup_step=user_data.setup_step,
            user_type=user_data.user_type,
            is_active=True,
            is_verified=False,
            activity_level=user_data.activity_level,
            height=user_data.height,
            weight=user_data.weight,
            height_unit=user_data.height_unit,
            weight_unit=user_data.weight_unit,
            profile_version=user_data.profile_version,
            flagged_for_review=False,
            joined_at=datetime.utcnow(),
            accepted_terms_at=datetime.utcnow() if user_data.accepted_terms else None,
            accepted_privacy_policy_at=datetime.utcnow() if user_data.accepted_privacy_policy else None,
            age=user_data.age,
            gender=user_data.gender,
            email_notifications=user_data.email_notifications,
            push_notifications=user_data.push_notifications,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User created successfully: {new_user.id}")
        return new_user

    except HTTPException as e:
        logger.error(f"User creation failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during user creation")
        raise HTTPException(status_code=500, detail="User registration failed. Please try again.")

def get_user_by_email(db: Session, email: str) -> User:
    """ Retrieves a user by email. """
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"User not found for email: {email}")
        return user
    except Exception as e:
        logger.exception("Error retrieving user by email")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")

def get_user_by_username(db: Session, username: str) -> User:
    """ Retrieves a user by username. """
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            logger.warning(f"User not found for username: {username}")
        return user
    except Exception as e:
        logger.exception("Error retrieving user by username")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")

def get_current_user(db: Session, user_id: UUID) -> User:
    """ Retrieves the currently authenticated user. """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.exception("Error retrieving current user")
        raise HTTPException(status_code=500, detail="Failed to retrieve user")

def update_last_login(user: User, db: Session):
    """ Updates the last login timestamp for a user. """
    try:
        user.last_login = datetime.utcnow()
        db.commit()
        logger.info(f"Updated last login for user: {user.id}")
    except Exception as e:
        logger.exception("Error updating last login")
        raise HTTPException(status_code=500, detail="Failed to update last login")

def enable_mfa(user: User, db: Session):
    """ Enables MFA for a user and generates a secret. """
    try:
        mfa_data = generate_mfa_secret(user.email)
        user.mfa_secret = mfa_data["mfa_secret"]
        user.mfa_enabled = True
        db.commit()
        return {"message": "MFA enabled", "qr_code": mfa_data["qr_code"], "manual_key": mfa_data["manual_key"]}
    except Exception as e:
        logger.exception(f"Error enabling MFA: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to enable MFA")

def disable_mfa(user: User, db: Session):
    """ Disables MFA for a user. """
    try:
        user.mfa_secret = None
        user.mfa_enabled = False
        db.commit()
        return {"message": "MFA disabled successfully"}
    except Exception as e:
        logger.exception(f"Error disabling MFA: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to disable MFA")

def generate_password_reset_token(user_id: UUID) -> str:
    """ Generates a password reset token for the user. """
    import jwt
    from backend.core.config import settings

    try:
        token_data = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + settings.PASSWORD_RESET_EXPIRATION,
        }
        token = jwt.encode(token_data, settings.SECRET_KEY, algorithm="HS256")
        logger.info(f"Generated password reset token for user: {user_id}")
        return token
    except Exception as e:
        logger.exception("Error generating password reset token")
        raise HTTPException(status_code=500, detail="Failed to generate password reset token")

def update_password(user_id: UUID, new_password: str, db: Session):
    """ Updates a user's password. """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = hash_password(new_password)
        db.commit()
        logger.info(f"Password updated for user: {user.id}")
    except Exception as e:
        logger.exception("Error updating password")
        raise HTTPException(status_code=500, detail="Failed to update password")

def create_user_session(user: User, db: Session, is_mobile: bool = False):
    """ Creates a session for a user upon login. """
    try:
        session_token = create_session(user.id, db, is_mobile)
        return {"access_token": session_token, "token_type": "bearer"}
    except Exception as e:
        logger.exception("Error creating user session")
        raise HTTPException(status_code=500, detail="Failed to create user session")

def admin_required(current_user: User = Depends(get_current_user)):
    """ Middleware to ensure that only admins can access a route. """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied. Admins only.")
