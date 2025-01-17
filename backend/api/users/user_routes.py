from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.users.user_service import update_user_profile, get_user_profile
from backend.schemas.user_schema import UserProfileUpdate, UserProfile
from backend.core.aws_utils import upload_file_to_s3
from backend.models.user import User
from backend.api.auth.auth_service import get_current_user

router = APIRouter()


# Update user profile
@router.put("/profile", response_model=UserProfile)
async def update_profile(
        profile_data: UserProfileUpdate = Depends(),
        file: UploadFile = File(None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    profile_picture_url = None
    if file:
        filename = f"profile_pictures/{current_user.id}/{file.filename}"
        profile_picture_url = upload_file_to_s3(file, filename)

    updated_user = update_user_profile(db, current_user.id, profile_data, profile_picture_url)
    return updated_user


# Get user profile
@router.get("/profile", response_model=UserProfile)
async def get_profile(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    return get_user_profile(db, current_user.id)
