from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends

from backend.api.auth.auth_service import hash_password, get_current_user
from backend.models.user import User, UserType
from backend.schemas.user_schema import UserCreate
from backend.core.logging_config import get_logger

logger = get_logger(__name__)


def create_admin_user(db: Session, user_data: UserCreate):
    """ Create a new admin user securely. """
    try:
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")

        hashed_password = hash_password(user_data.password)

        admin_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            is_active=True,
            is_verified=True,
            subscription_plan="Free",
            user_type=UserType.ADMIN,
            admin_secret_key=user_data.admin_secret_key,
            accepted_terms=True,
            accepted_privacy_policy=True,
            setup_step="completed",
            joined_at=datetime.utcnow(),
            accepted_terms_at=datetime.utcnow(),
            accepted_privacy_policy_at=datetime.utcnow(),
            profile_version=1,
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        logger.info(f"Admin user created successfully: {admin_user.username}")
        return admin_user

    except SQLAlchemyError as e:
        logger.error(f"Database error during admin creation: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred while creating admin user")
    except Exception as e:
        logger.exception("Unexpected error during admin creation")
        raise HTTPException(status_code=500, detail="Unexpected error occurred while creating admin user")


def list_admin_users(db: Session):
    """ Retrieve a list of all admin users. """
    try:
        admins = db.query(User).filter(User.user_type == UserType.ADMIN).all()
        if not admins:
            raise HTTPException(status_code=404, detail="No admin users found")

        logger.info(f"Retrieved {len(admins)} admin users")
        return admins
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving admin users: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error while retrieving admin users")
    except Exception as e:
        logger.exception("Unexpected error retrieving admin users")
        raise HTTPException(status_code=500, detail="Unexpected error while retrieving admin users")


def moderate_flagged_users(db: Session):
    """ Retrieve a list of users flagged for review. """
    try:
        flagged_users = db.query(User).filter(User.flagged_for_review == True).all()
        if not flagged_users:
            raise HTTPException(status_code=404, detail="No flagged users found")

        logger.info(f"Retrieved {len(flagged_users)} flagged users")
        return flagged_users
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving flagged users: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error while retrieving flagged users")
    except Exception as e:
        logger.exception("Unexpected error retrieving flagged users")
        raise HTTPException(status_code=500, detail="Unexpected error while retrieving flagged users")

