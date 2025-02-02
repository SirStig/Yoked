import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend.models.session import SessionModel as SessionModel
from backend.core.logging_config import get_logger
from backend.schemas.session_schema import UserSession
from uuid import UUID

# Logger setup
logger = get_logger(__name__)

# Session durations
WEB_SESSION_DURATION = timedelta(days=7)  # Web session duration
MOBILE_SESSION_DURATION = timedelta(days=365)  # Mobile session duration

### **Generate Unique Session Token**
def generate_token() -> str:
    """Generate a unique session token."""
    token = str(uuid.uuid4())
    logger.debug(f"Generated session token: {token}")
    return token

### **Create a New Session**
def create_session(user_id: UUID, db: Session, is_mobile: bool = False, mfa_verified: bool = False, device_type: str = None, location: str = None, ip_address: str = None) -> str:
    """
    Create a new session for the user or return an existing active session.
    """
    logger.info(f"Creating or fetching session for user_id: {user_id}, is_mobile: {is_mobile}")

    try:
        existing_session = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.is_mobile == is_mobile,
            SessionModel.expires_at > datetime.utcnow()
        ).first()

        if existing_session:
            return existing_session.token

        token = generate_token()
        expires_at = datetime.utcnow() + (MOBILE_SESSION_DURATION if is_mobile else WEB_SESSION_DURATION)

        new_session = SessionModel(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_mobile=is_mobile,
            mfa_verified=mfa_verified,
            device_type=device_type,
            location=location,
            ip_address=ip_address,
            last_activity=datetime.utcnow()
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return token

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create session")

### **Validate a Session Token**
def validate_session(token: str, db: Session) -> SessionModel:
    """
    Validate a session token.
    """
    session = db.query(SessionModel).filter(SessionModel.token == token).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session not found")
    if session.expires_at < datetime.utcnow():
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    session.last_activity = datetime.utcnow()
    db.commit()
    return session

### **Invalidate All User Sessions**
def invalidate_session(user_id: UUID, db: Session, is_mobile: bool = None):
    """
    Invalidate all sessions for the user or optionally only for web or mobile.
    """
    try:
        query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
        if is_mobile is not None:
            query = query.filter(SessionModel.is_mobile == is_mobile)
        query.delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to invalidate sessions")

### **Invalidate a Specific Session**
def invalidate_specific_session(token: str, db: Session):
    """
    Invalidate a specific session.
    """
    try:
        session = db.query(SessionModel).filter(SessionModel.token == token).first()
        if session:
            db.delete(session)
            db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to invalidate session")
