from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from backend.core.database import Base
from backend.core.config import settings
from jose import jwt

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    user = relationship("User")

    @staticmethod
    def create_token(user_id: int, db, lifetime_minutes: int = 60):
        token = jwt.encode(
            {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(minutes=lifetime_minutes)},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        session = Session(user_id=user_id, token=token, expires_at=datetime.utcnow() + timedelta(minutes=lifetime_minutes))
        db.add(session)
        db.commit()
        return token
