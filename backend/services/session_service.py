import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend.models.session import SessionModel
from backend.core.logging_config import get_logger
from backend.schemas.session_schema import UserSession
from uuid import UUID

# Logger setup
logger = get_logger(__name__)

# Session durations
WEB_SESSION_DURATION = timedelta(days=7)  # Web session duration
MOBILE_SESSION_DURATION = timedelta(days=365)  # Mobile session duration

def generate_token() -> str:
    """Generate a unique session token."""
    token = str(uuid.uuid4())
    logger.debug(f"Generated session token: {token}")
    return token

def create_session(
    user_id: UUID,
    db: Session,
    is_mobile: bool = False,
    mfa_verified: bool = False,
    device_type: str = None,
    device_os: str = None,
    browser: str = None,
    location: str = None,
    ip_address: str = None
) -> str:
    """
    Create a new session for the user or return an existing active session on the same device.
    """
    logger.info(f"Creating or fetching session for user_id: {user_id}, is_mobile: {is_mobile}")

    try:
        # Look for an existing active session with matching device details
        existing_session = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.is_mobile == is_mobile,
            SessionModel.expires_at > datetime.utcnow(),
            SessionModel.device_type == device_type,
            SessionModel.device_os == device_os,
            SessionModel.browser == browser,
            SessionModel.ip_address == ip_address
        ).first()

        if existing_session:
            logger.info(f"Reusing active session for user_id: {user_id}, session_id: {existing_session.id}")
            return existing_session.token

        # No active session found; create a new one
        token = generate_token()
        expires_at = datetime.utcnow() + (MOBILE_SESSION_DURATION if is_mobile else WEB_SESSION_DURATION)
        logger.debug(f"Creating new session with expiry: {expires_at}")

        new_session = SessionModel(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_mobile=is_mobile,
            mfa_verified=mfa_verified,
            device_type=device_type,
            device_os=device_os,
            browser=browser,
            location=location,
            ip_address=ip_address,
            last_activity=datetime.utcnow(),
            is_active=True  # New field to track active/inactive sessions
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        logger.info(f"New session created for user_id: {user_id}, session_id: {new_session.id}")
        return token

    except SQLAlchemyError as e:
        logger.error(f"Failed to create or fetch session for user_id: {user_id}. Error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create session")

def validate_session(token: str, db: Session) -> UserSession:
    """
    Validate a session token and ensure it's active.
    """
    logger.debug(f"Validating session token: {token}")
    session = db.query(SessionModel).filter(SessionModel.token == token, SessionModel.is_active == True).first()

    if not session:
        logger.warning(f"Session token not found or inactive: {token}")
        raise HTTPException(status_code=401, detail="Session not found or inactive")

    if session.expires_at < datetime.utcnow():
        session.is_active = False
        db.commit()
        logger.warning(f"Session expired: {token}, expires_at: {session.expires_at}")
        raise HTTPException(status_code=401, detail="Session expired")

    session.last_activity = datetime.utcnow()
    db.commit()

    logger.info(f"Session validated: {session.id}, user_id: {session.user_id}")
    return UserSession.model_validate(session)

def deactivate_session(user_id: UUID, db: Session, is_mobile: bool = None):
    """
    Deactivate all sessions for the user or optionally only for web or mobile.
    """
    logger.info(f"Deactivating sessions for user_id: {user_id}, is_mobile: {is_mobile}")
    try:
        query = db.query(SessionModel).filter(SessionModel.user_id == user_id, SessionModel.is_active == True)
        if is_mobile is not None:
            query = query.filter(SessionModel.is_mobile == is_mobile)
        updated_count = query.update({SessionModel.is_active: False})
        db.commit()
        logger.info(f"Deactivated {updated_count} session(s) for user_id: {user_id}")
    except SQLAlchemyError as e:
        logger.error(f"Failed to deactivate sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to deactivate sessions")

def deactivate_specific_session(token: str, db: Session):
    """
    Deactivate a specific session.
    """
    logger.info(f"Deactivating specific session token: {token}")
    try:
        session = db.query(SessionModel).filter(SessionModel.token == token, SessionModel.is_active == True).first()
        if session:
            session.is_active = False
            db.commit()
            logger.info(f"Session deactivated: {token}")
        else:
            logger.warning(f"Session token not found or already inactive: {token}")
    except SQLAlchemyError as e:
        logger.error(f"Failed to deactivate session token: {token}, error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to deactivate session")

def get_active_sessions(user_id: UUID, db: Session, is_mobile: bool = None):
    """
    Retrieve active sessions for the user.
    """
    logger.debug(f"Fetching active sessions for user_id: {user_id}, is_mobile: {is_mobile}")
    try:
        query = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.is_active == True
        )
        if is_mobile is not None:
            query = query.filter(SessionModel.is_mobile == is_mobile)
        sessions = query.all()

        session_list = [UserSession.model_validate(session) for session in sessions]
        logger.info(f"Retrieved {len(session_list)} active session(s) for user_id: {user_id}")
        return session_list
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch active sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch active sessions")

def fetch_user_sessions(user_id: UUID, db: Session):
    """
    Fetch all user sessions, both active and inactive.
    """
    logger.info(f"Fetching all sessions for user_id: {user_id}")
    try:
        sessions = db.query(SessionModel).filter(SessionModel.user_id == user_id).all()

        session_data = [UserSession.model_validate(session) for session in sessions]
        logger.info(f"Fetched {len(session_data)} session(s) for user_id: {user_id}")
        return session_data
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sessions")
