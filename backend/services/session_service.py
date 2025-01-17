from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from backend.models.session import Session

def create_session(user_id: int, db: Session, lifetime_minutes: int = 60):
    return Session.create_token(user_id, db, lifetime_minutes)

def validate_session(token: str, db: Session):
    session = db.query(Session).filter(Session.token == token, Session.expires_at > datetime.utcnow()).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    return session.user
