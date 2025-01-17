from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user_schema import UserProfileUpdate


def update_user_profile(db: Session, user_id: int, profile_data: UserProfileUpdate, profile_picture_url: str = None):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    if profile_data.bio is not None:
        user.bio = profile_data.bio
    if profile_data.fitness_goals is not None:
        user.fitness_goals = profile_data.fitness_goals
    if profile_picture_url is not None:
        user.profile_picture = profile_picture_url

    db.commit()
    db.refresh(user)
    return user


def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
