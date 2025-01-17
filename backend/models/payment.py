from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from backend.core.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stripe_payment_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
