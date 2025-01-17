from sqlalchemy.orm import Session
from datetime import datetime
from backend.core.database import SessionLocal
from backend.models.session import Session

def cleanup_expired_sessions():
    db: Session = SessionLocal()
    db.query(Session).filter(Session.expires_at < datetime.utcnow()).delete()
    db.commit()
    db.close()
