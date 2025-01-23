from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.api.auth.auth_service import hash_password
from backend.models.user import User, UserType, SetupStep
from backend.schemas.user_schema import UserCreate
from backend.core.logging_config import get_logger

logger = get_logger(__name__)

def create_admin_user(db: Session, user_data: UserCreate):
    """
    Create a new admin user.

    Args:
        db (Session): Database session.
        user_data (UserCreate): User creation data.

    Returns:
        User: The created admin user.

    Raises:
        Exception: If an error occurs during user creation.
    """
    logger.debug(f"Starting admin creation. User data: {user_data}")
    try:
        hashed_password = hash_password(user_data.hashed_password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            # Admin-specific defaults
            is_active=True,
            is_verified=True,
            subscription_plan="Free",
            user_type=UserType.ADMIN,
            admin_secret_key=user_data.admin_secret_key,
            # Required fields
            accepted_terms=True,
            accepted_privacy_policy=True,
            # Setup step defaults for admin
            setup_step="completed",
            # Timestamps
            joined_at=datetime.utcnow(),
            accepted_terms_at=datetime.utcnow(),
            accepted_privacy_policy_at=datetime.utcnow(),
            # Versioning
            profile_version=1,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"Admin user created: {user.username} (ID: {user.id})")
        return user

    except SQLAlchemyError as e:
        logger.error(f"Database error during admin user creation: {str(e)}")
        db.rollback()  # Rollback transaction to maintain database integrity
        raise Exception("Database error occurred while creating admin user")
    except Exception as e:
        logger.exception(f"Unexpected error during admin user creation: {str(e)}")
        raise Exception("Unexpected error occurred while creating admin user")



def list_admin_users(db: Session):
    """
    Retrieve a list of all admin users.

    Args:
        db (Session): Database session.

    Returns:
        list: List of admin users.
    """
    try:
        admins = db.query(User).filter(User.user_type == UserType.ADMIN).all()
        logger.info(f"Retrieved {len(admins)} admin users")
        return admins

    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving admin users: {str(e)}")
        raise Exception("Database error occurred while retrieving admin users")
    except Exception as e:
        logger.exception(f"Unexpected error while retrieving admin users: {str(e)}")
        raise Exception("Unexpected error occurred while retrieving admin users")


def moderate_flagged_users(db: Session):
    """
    Retrieve a list of users flagged for review.

    Args:
        db (Session): Database session.

    Returns:
        list: List of flagged users.
    """
    try:
        flagged_users = db.query(User).filter(User.flagged_for_review == True).all()
        logger.info(f"Retrieved {len(flagged_users)} flagged users")
        return flagged_users

    except SQLAlchemyError as e:
        logger.error(f"Database error while retrieving flagged users: {str(e)}")
        raise Exception("Database error occurred while retrieving flagged users")
    except Exception as e:
        logger.exception(f"Unexpected error while retrieving flagged users: {str(e)}")
        raise Exception("Unexpected error occurred while retrieving flagged users")
