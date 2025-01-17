from sqlalchemy.orm import Session
from backend.models.workout import Workout
from backend.schemas.workout_schema import WorkoutCreate

def create_workout(db: Session, workout_data: WorkoutCreate) -> Workout:
    workout = Workout(**workout_data.dict())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

def get_workout_by_id(db: Session, workout_id: int) -> Workout:
    return db.query(Workout).filter(Workout.id == workout_id).first()

def update_workout(db: Session, workout_id: int, workout_data: WorkoutCreate) -> Workout:
    workout = get_workout_by_id(db, workout_id)
    if not workout:
        return None
    for key, value in workout_data.dict().items():
        setattr(workout, key, value)
    db.commit()
    db.refresh(workout)
    return workout

def delete_workout(db: Session, workout_id: int):
    workout = get_workout_by_id(db, workout_id)
    if workout:
        db.delete(workout)
        db.commit()
