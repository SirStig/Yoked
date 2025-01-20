from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, UUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from backend.core.database import Base
import datetime

class PaymentPlatform(PyEnum):
    STRIPE = "Stripe"
    GOOGLE = "Google"
    APPLE = "Apple"

class PaymentStatus(PyEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    stripe_payment_id = Column(String, nullable=True)
    google_payment_id = Column(String, nullable=True)
    apple_payment_id = Column(String, nullable=True)

    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    platform = Column(Enum(PaymentPlatform), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    subscription_tier_id = Column(UUID(as_uuid=True), ForeignKey("subscription_tiers.id"), nullable=False)

    renewal_date = Column(DateTime, nullable=True)

    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="payments")
    subscription_tier = relationship("SubscriptionTier")

    def __repr__(self):
        return (
            f"<Payment(id={self.id}, user_id={self.user_id}, platform={self.platform}, "
            f"amount={self.amount}, status={self.status}, subscription_tier={self.subscription_tier})>"
        )
