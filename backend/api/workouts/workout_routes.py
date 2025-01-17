from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.api.workouts.workout_service import (
    create_workout,
    get_workout_by_id,
    update_workout,
    delete_workout,
)
from backend.schemas.workout_schema import WorkoutCreate, WorkoutResponse

router = APIRouter()

@router.post("/", response_model=WorkoutResponse)
def create_new_workout(workout_data: WorkoutCreate, db: Session = Depends(get_db)):
    return create_workout(db, workout_data)

@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = get_workout_by_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_existing_workout(workout_id: int, workout_data: WorkoutCreate, db: Session = Depends(get_db)):
    updated_workout = update_workout(db, workout_id, workout_data)
    if not updated_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return updated_workout

@router.delete("/{workout_id}")
def remove_workout(workout_id: int, db: Session = Depends(get_db)):
    delete_workout(db, workout_id)
    return {"message": "Workout deleted successfully"}
