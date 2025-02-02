from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

from backend.models.user import User
from backend.schemas.user_schema import UserProfileUpdate
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

### **Get User Profile**
def get_user_profile(db: Session, user_id: UUID) -> User:
    """ Fetch a user's profile. """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

### **Update User Profile**
def update_user_profile(db: Session, user_id: UUID, profile_data: UserProfileUpdate) -> User:
    """ Update a user's profile. """
    try:
        user = get_user_profile(db, user_id)
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(user, field, value)
        user.profile_version += 1
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        logger.error(f"Database error while updating profile: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

### **Deactivate User Account**
def deactivate_user(db: Session, user_id: UUID):
    """ Deactivate a user's account. """
    try:
        user = get_user_profile(db, user_id)
        user.is_active = False
        user.profile_version += 1
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error while deactivating user: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

### **Reactivate User Account**
def reactivate_user(db: Session, user_id: UUID):
    """ Reactivate a user's account. """
    try:
        user = get_user_profile(db, user_id)
        user.is_active = True
        user.profile_version += 1
        db.commit()
    except SQLAlchemyError as e:
        logger.error(f"Database error while reactivating user: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

### **Check if User is Active**
def is_user_active(db: Session, user_id: UUID) -> bool:
    """ Check if a user account is active. """
    return get_user_profile(db, user_id).is_active
