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

def generate_token() -> str:
    """Generate a unique session token."""
    token = str(uuid.uuid4())
    logger.debug(f"Generated session token: {token}")
    return token

def create_session(user_id: UUID, db: Session, is_mobile: bool = False, mfa_verified: bool = False, device_type: str = None, location: str = None, ip_address: str = None) -> str:
    """
    Create a new session for the user or return an existing active session.
    """
    logger.info(f"Creating or fetching session for user_id: {user_id}, is_mobile: {is_mobile}")

    try:
        # Look for an existing session that has not expired
        existing_session = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.is_mobile == is_mobile,
            SessionModel.expires_at > datetime.utcnow()
        ).first()

        if existing_session:
            logger.info(f"Active session found for user_id: {user_id}, session_id: {existing_session.id}")
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
            location=location,
            ip_address=ip_address,
            last_activity=datetime.utcnow()
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

def validate_session(token: str, db: Session) -> SessionModel:
    """
    Validate a session token.
    - token: The session token to validate.
    - db: Database session.
    """
    logger.debug(f"Validating session token: {token}")
    session = db.query(SessionModel).filter(SessionModel.token == token).first()

    if not session:
        logger.warning(f"Session token not found: {token}")
        raise HTTPException(status_code=401, detail="Session not found")
    if session.expires_at < datetime.utcnow():
        logger.warning(f"Session expired: {token}, expires_at: {session.expires_at}")
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    session.last_activity = datetime.utcnow()
    db.commit()

    logger.info(f"Session validated: {session.id}, user_id: {session.user_id}")
    return session

def invalidate_session(user_id: UUID, db: Session, is_mobile: bool = None):
    """
    Invalidate all sessions for the user or optionally only for web or mobile.
    - user_id: UUID of the user.
    - db: Database session.
    - is_mobile: If specified, filter by session type (web/mobile).
    """
    logger.info(f"Invalidating sessions for user_id: {user_id}, is_mobile: {is_mobile}")
    try:
        query = db.query(SessionModel).filter(SessionModel.user_id == user_id)
        if is_mobile is not None:
            query = query.filter(SessionModel.is_mobile == is_mobile)
        deleted_count = query.delete()
        db.commit()
        logger.info(f"Invalidated {deleted_count} session(s) for user_id: {user_id}")
    except SQLAlchemyError as e:
        logger.error(f"Failed to invalidate sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to invalidate sessions")

def invalidate_specific_session(token: str, db: Session):
    """
    Invalidate a specific session.
    - token: Session token to invalidate.
    - db: Database session.
    """
    logger.info(f"Invalidating specific session token: {token}")
    try:
        # Ensure the token is treated as a string
        session = db.query(SessionModel).filter(SessionModel.token == token).first()
        if session:
            db.delete(session)
            db.commit()
            logger.info(f"Session invalidated: {token}")
        else:
            logger.warning(f"Session token not found for invalidation: {token}")
    except SQLAlchemyError as e:
        logger.error(f"Failed to invalidate session token: {token}, error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to invalidate session")

def get_active_sessions(user_id: UUID, db: Session, is_mobile: bool = None):
    """
    Retrieve active sessions for the user.
    - user_id: UUID of the user.
    - db: Database session.
    - is_mobile: If specified, filter by session type (web/mobile).
    """
    logger.debug(f"Fetching active sessions for user_id: {user_id}, is_mobile: {is_mobile}")
    try:
        query = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.expires_at > datetime.utcnow(),
        )
        if is_mobile is not None:
            query = query.filter(SessionModel.is_mobile == is_mobile)
        sessions = query.all()

        # Map sessions to schema for output
        session_list = [
            UserSession(
                id=session.id,
                user_id=session.user_id,
                token=session.token,
                created_at=session.created_at,
                expires_at=session.expires_at,
                is_mobile=session.is_mobile,
                mfa_verified=session.mfa_verified,
                device_type=session.device_type,
                location=session.location,
                ip_address=session.ip_address,
                last_activity=session.last_activity,
            )
            for session in sessions
        ]

        logger.info(f"Retrieved {len(session_list)} active session(s) for user_id: {user_id}")
        return session_list
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch active sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch active sessions")

def fetch_user_sessions(user_id: UUID, db: Session):
    """
    Fetch all active sessions for a user.
    :param user_id: The ID of the user whose sessions to fetch.
    :param db: The database session.
    :return: List of UserSession objects.
    """
    logger.info(f"Fetching active sessions for user_id: {user_id}")
    try:
        sessions = db.query(SessionModel).filter(
            SessionModel.user_id == user_id,
            SessionModel.expires_at > datetime.utcnow()
        ).all()

        session_data = [
            UserSession(
                id=session.id,
                user_id=session.user_id,
                token=session.token,
                created_at=session.created_at,
                expires_at=session.expires_at,
                is_mobile=session.is_mobile,
                mfa_verified=session.mfa_verified,
                device_type=session.device_type,
                location=session.location,
                ip_address=session.ip_address,
                last_activity=session.last_activity,
            )
            for session in sessions
        ]

        logger.info(f"Fetched {len(session_data)} session(s) for user_id: {user_id}")
        return session_data
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch sessions")

