from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from backend.models.user import User
from backend.schemas.user_schema import UserProfileUpdate
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)


def get_user_profile(db: Session, user_id: UUID) -> User:
    logger.debug(f"Fetching profile for user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching profile for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error while fetching profile for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


def update_user_profile(
    db: Session, user_id: UUID, profile_data: UserProfileUpdate, profile_picture_url: str = None
) -> User:
    """
    Update a user's profile with the provided data.
    """
    logger.debug(f"Updating profile for user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found for profile update")
            raise HTTPException(status_code=404, detail="User not found")

        # Update user fields
        for field, value in profile_data.dict(exclude_unset=True).items():
            if hasattr(user, field):
                setattr(user, field, value)
            else:
                logger.warning(f"Field {field} does not exist on User model.")

        if profile_picture_url:
            user.profile_picture = profile_picture_url

        # Increment profile version
        user.profile_version = (user.profile_version or 0) + 1
        logger.debug(f"Incremented profile version for user ID {user_id} to {user.profile_version}")

        db.commit()
        db.refresh(user)
        logger.info(f"Profile updated successfully for user ID {user_id}")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating profile for user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error while updating profile for user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


def deactivate_user(db: Session, user_id: UUID):
    """
    Deactivate a user's account (soft delete).
    """
    logger.debug(f"Deactivating user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found for deactivation")
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = False

        # Increment profile version
        user.profile_version = (user.profile_version or 0) + 1
        logger.debug(f"Incremented profile version for user ID {user_id} to {user.profile_version}")

        db.commit()
        logger.info(f"User ID {user_id} deactivated successfully")
    except SQLAlchemyError as e:
        logger.error(f"Database error while deactivating user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error while deactivating user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


def reactivate_user(db: Session, user_id: UUID):
    """
    Reactivate a user's account.
    """
    logger.debug(f"Reactivating user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found for reactivation")
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = True

        # Increment profile version
        user.profile_version = (user.profile_version or 0) + 1
        logger.debug(f"Incremented profile version for user ID {user_id} to {user.profile_version}")

        db.commit()
        logger.info(f"User ID {user_id} reactivated successfully")
    except SQLAlchemyError as e:
        logger.error(f"Database error while reactivating user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error while reactivating user ID {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


def is_user_active(db: Session, user_id: UUID) -> bool:
    """
    Check if a user's account is active.
    """
    logger.debug(f"Checking active status for user ID {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found for active status check")
            raise HTTPException(status_code=404, detail="User not found")
        return user.is_active
    except SQLAlchemyError as e:
        logger.error(f"Database error while checking active status for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.exception(f"Unexpected error while checking active status for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")
