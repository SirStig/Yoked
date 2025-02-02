import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.auth.auth_service import get_current_user
from backend.models import User
from backend.schemas.user_schema import UserProfileUpdate, UserProfile
from backend.api.users.user_service import (
    deactivate_user,
    reactivate_user,
    is_user_active,
    get_user_profile,
    update_user_profile,
)
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

# Router setup
router = APIRouter(prefix="/api/users", tags=["Users"])

### **Get User Profile**
@router.get("/profile", response_model=UserProfile)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Fetch the current user's profile. """
    try:
        logger.info(f"Fetching profile for user ID {current_user.id}")
        return get_user_profile(db, current_user.id)
    except Exception as e:
        logger.exception(f"Error fetching profile for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile.")

### **Get Profile Version**
@router.get("/profile/version", response_model=dict)
async def get_profile_version(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Get the profile version for the current user. """
    try:
        logger.info(f"Fetching profile version for user ID {current_user.id}")
        return {"profile_version": current_user.profile_version}
    except Exception as e:
        logger.exception(f"Error fetching profile version for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch profile version.")

### **Update User Profile**
@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Update the current user's profile. """
    try:
        logger.info(f"Updating profile for user ID {current_user.id}")
        return update_user_profile(db, current_user.id, profile_data)
    except Exception as e:
        logger.exception(f"Error updating profile for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile.")

### **Deactivate User Account**
@router.put("/deactivate", response_model=dict)
async def deactivate_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Deactivate the current user's account. """
    try:
        logger.info(f"Deactivating account for user ID {current_user.id}")
        deactivate_user(db, current_user.id)
        return {"message": "Account deactivated successfully."}
    except Exception as e:
        logger.exception(f"Error deactivating account for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to deactivate account.")

### **Reactivate User Account (Admin Only)**
@router.put("/reactivate", response_model=dict)
async def reactivate_account(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    """ Reactivate a user's account (Admin only). """
    try:
        logger.info(f"Reactivating account for user ID {user_id}")
        reactivate_user(db, user_id)
        return {"message": "Account reactivated successfully."}
    except Exception as e:
        logger.exception(f"Error reactivating account for user ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to reactivate account.")

### **Check if User is Active**
@router.get("/active-status", response_model=dict)
async def check_active_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """ Check if the current user's account is active. """
    try:
        logger.info(f"Checking active status for user ID {current_user.id}")
        return {"is_active": is_user_active(db, current_user.id)}
    except Exception as e:
        logger.exception(f"Error checking active status for user ID {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check active status.")
