import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend.models.session import Session as SessionModel
from backend.core.logging_config import get_logger
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


def create_session(user_id: UUID, db: Session, is_mobile: bool = False) -> str:
    """
    Create a new session for the user.
    - user_id: UUID of the user.
    - db: Database session.
    - is_mobile: Indicates if the session is for mobile.
    """
    logger.info(f"Creating session for user_id: {user_id}, is_mobile: {is_mobile}")
    token = generate_token()
    expires_at = datetime.utcnow() + (MOBILE_SESSION_DURATION if is_mobile else WEB_SESSION_DURATION)
    logger.debug(f"Session will expire at: {expires_at}")

    try:
        session = SessionModel(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_mobile=is_mobile,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        logger.info(f"Session created: {session.id}, expires_at: {expires_at}")
        return token
    except SQLAlchemyError as e:
        logger.error(f"Failed to create session for user_id: {user_id}, error: {e}")
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
        logger.info(f"Retrieved {len(sessions)} active session(s) for user_id: {user_id}")
        return sessions
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch active sessions for user_id: {user_id}, error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch active sessions")
