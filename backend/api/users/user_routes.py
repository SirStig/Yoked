from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user
from backend.schemas.user_schema import UserProfileUpdate, UserProfile
from backend.models.user import User
from backend.api.users.user_service import (
    get_user_profile,
    update_user_profile,
    deactivate_user,
    reactivate_user,
    is_user_active,
)
from backend.core.aws_utils import upload_file_to_s3
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's profile.
    """
    logger.info(f"Fetching profile for user ID {current_user.id}")
    try:
        return UserProfile.from_orm(current_user)
    except HTTPException as e:
        logger.error(f"Error fetching profile for user ID {current_user.id}: {e.detail}")
        raise e



@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the current user's profile.
    """
    logger.info(f"Updating profile for user ID {current_user.id}")
    try:
        if profile_data.age is not None:
            current_user.age = profile_data.age
        if profile_data.gender is not None:
            current_user.gender = profile_data.gender
        if profile_data.fitness_goals is not None:
            current_user.fitness_goals = profile_data.fitness_goals
        if profile_data.height is not None:
            current_user.height = profile_data.height
        if profile_data.weight is not None:
            current_user.weight = profile_data.weight
        if profile_data.height_unit is not None:
            current_user.height_unit = profile_data.height_unit
        if profile_data.weight_unit is not None:
            current_user.weight_unit = profile_data.weight_unit
        if profile_data.setup_step is not None:
            current_user.setup_step = profile_data.setup_step

        db.commit()
        db.refresh(current_user)

        logger.info(f"Profile updated for user ID {current_user.id}")
        return UserProfile.from_orm(current_user)
    except Exception as e:
        logger.error(f"Error updating profile for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile.")


@router.put("/deactivate", response_model=dict)
async def deactivate_account(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Deactivate the current user's account.
    """
    logger.info(f"Deactivating account for user ID {current_user.id}")
    try:
        deactivate_user(db, current_user.id)
        logger.info(f"Account deactivated for user ID {current_user.id}")
        return {"message": "Account deactivated successfully"}
    except HTTPException as e:
        logger.error(f"Error deactivating account for user ID {current_user.id}: {e.detail}")
        raise e


@router.put("/reactivate", response_model=dict)
async def reactivate_account(
    user_id: int, db: Session = Depends(get_db)
):
    """
    Reactivate a user's account (admin feature).
    """
    logger.info(f"Reactivating account for user ID {user_id}")
    try:
        reactivate_user(db, user_id)
        logger.info(f"Account reactivated for user ID {user_id}")
        return {"message": "Account reactivated successfully"}
    except HTTPException as e:
        logger.error(f"Error reactivating account for user ID {user_id}: {e.detail}")
        raise e


@router.get("/active-status", response_model=dict)
async def check_active_status(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Check if the current user's account is active.
    """
    logger.info(f"Checking active status for user ID {current_user.id}")
    try:
        is_active = is_user_active(db, current_user.id)
        logger.info(f"Active status for user ID {current_user.id}: {is_active}")
        return {"is_active": is_active}
    except HTTPException as e:
        logger.error(f"Error checking active status for user ID {current_user.id}: {e.detail}")
        raise e
