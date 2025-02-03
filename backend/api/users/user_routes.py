import uuid
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user
from backend.schemas.user_schema import UserProfileUpdate, UserOut
from backend.models.user import User
from backend.api.users.user_service import (
    deactivate_user,
    reactivate_user,
    is_user_active,
)
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter()


@router.get("/profile", response_model=UserOut)
async def get_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Fetch the current user's profile.
    """
    logger.info(f"Fetching profile for user ID {current_user.id}")
    try:
        return UserOut.from_orm(current_user)
    except Exception as e:
        logger.exception(f"Error fetching profile for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile.")


@router.get("/profile/version", response_model=dict)
async def get_profile_version(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get the profile version for the current user.
    """
    logger.info(f"Fetching profile version for user ID {current_user.id}")
    try:
        return {"profile_version": current_user.profile_version}
    except Exception as e:
        logger.exception(f"Error fetching profile version for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile version.")


@router.put("/profile", response_model=UserOut)
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
        # Update user fields
        for key, value in profile_data.dict(exclude_unset=True).items():
            setattr(current_user, key, value)

        # Increment profile version
        current_user.profile_version += 1

        db.commit()
        db.refresh(current_user)

        logger.info(f"Profile updated for user ID {current_user.id}")
        return UserOut.from_orm(current_user)
    except Exception as e:
        logger.exception(f"Error updating profile for user ID {current_user.id}: {str(e)}")
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

        # Increment profile version
        current_user.profile_version += 1
        db.commit()

        logger.info(f"Account deactivated for user ID {current_user.id}")
        return {"message": "Account deactivated successfully"}
    except Exception as e:
        logger.exception(f"Error deactivating account for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deactivate account.")


@router.put("/reactivate", response_model=dict)
async def reactivate_account(
    user_id: uuid.UUID, db: Session = Depends(get_db)
):
    """
    Reactivate a user's account (admin feature).
    """
    logger.info(f"Reactivating account for user ID {user_id}")
    try:
        reactivate_user(db, user_id)

        # Increment profile version
        user = db.query(User).filter(User.id == user_id).first()
        user.profile_version += 1
        db.commit()

        logger.info(f"Account reactivated for user ID {user_id}")
        return {"message": "Account reactivated successfully"}
    except Exception as e:
        logger.exception(f"Error reactivating account for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to reactivate account.")


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
        return {"is_active": is_active}
    except Exception as e:
        logger.exception(f"Error checking active status for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check active status.")
