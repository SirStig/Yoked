from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.models.session import Session as SessionModel
from backend.schemas.user_schema import UserProfileUpdate
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)


def get_user_profile(db: Session, user_id: int) -> User:
    logger.debug(f"Fetching profile for user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    # Log the data returned by the database
    logger.debug(f"User data: {user.__dict__}")
    return user


def update_user_profile(
    db: Session, user_id: int, profile_data: UserProfileUpdate, profile_picture_url: str = None
) -> User:
    """
    Update a user's profile with the provided data.
    """
    logger.debug(f"Updating profile for user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found for profile update")
        raise HTTPException(status_code=404, detail="User not found")

    # Update user fields
    if profile_data.bio is not None:
        user.bio = profile_data.bio
    if profile_data.fitness_goals is not None:
        user.fitness_goals = profile_data.fitness_goals  # Correct mapping
    if profile_data.age is not None:
        user.age = profile_data.age
    if profile_data.gender is not None:
        user.gender = profile_data.gender
    if profile_data.activity_level is not None:
        user.activity_level = profile_data.activity_level
    if profile_data.height is not None:
        user.height = int(profile_data.height)
    if profile_data.weight is not None:
        user.weight = int(profile_data.weight)
    if profile_data.height_unit is not None:
        user.height_unit = profile_data.height_unit
    if profile_data.weight_unit is not None:
        user.weight_unit = profile_data.weight_unit
    if profile_picture_url is not None:
        user.profile_picture = profile_picture_url

    db.commit()
    db.refresh(user)
    logger.info(f"Profile updated successfully for user ID {user_id}")
    return user



def deactivate_user(db: Session, user_id: int):
    """
    Deactivate a user's account (soft delete).
    - user_id: ID of the user to deactivate.
    """
    logger.debug(f"Deactivating user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found for deactivation")
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    logger.info(f"User ID {user_id} deactivated successfully")


def reactivate_user(db: Session, user_id: int):
    """
    Reactivate a user's account.
    - user_id: ID of the user to reactivate.
    """
    logger.debug(f"Reactivating user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found for reactivation")
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = True
    db.commit()
    logger.info(f"User ID {user_id} reactivated successfully")


def is_user_active(db: Session, user_id: int) -> bool:
    """
    Check if a user's account is active.
    - user_id: ID of the user to check.
    """
    logger.debug(f"Checking active status for user ID {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found for active status check")
        raise HTTPException(status_code=404, detail="User not found")
    return user.is_active
