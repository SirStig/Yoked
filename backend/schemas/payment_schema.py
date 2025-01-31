from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional
from enum import Enum


# Enums for Payment Platform and Status
class PaymentPlatform(str, Enum):
    STRIPE = "STRIPE"
    GOOGLE = "GOOGLE"
    APPLE = "APPLE"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PAID = "PAID"
    COMPLETE = "COMPLETE"


# Payment Create Schema
class PaymentCreate(BaseModel):
    user_id: Optional[UUID4] = Field(None, description="The UUID of the user making the payment")
    platform: PaymentPlatform = Field(..., description="Payment platform used")
    amount: int = Field(..., description="Amount paid in cents")
    currency: str = Field(..., description="Currency of the payment")
    subscription_id: UUID4 = Field(..., description="ID of the user subscription being paid for")
    stripe_payment_id: Optional[str] = Field(None, description="Stripe payment ID, if applicable")
    google_payment_id: Optional[str] = Field(None, description="Google payment ID, if applicable")
    apple_payment_id: Optional[str] = Field(None, description="Apple payment ID, if applicable")
    renewal_date: Optional[datetime] = Field(None, description="Date of subscription renewal")

    class Config:
        from_attributes = True


# Payment Output Schema
class PaymentOut(BaseModel):
    id: UUID4 = Field(..., description="Unique payment ID")
    user_id: UUID4 = Field(..., description="The UUID of the user who made the payment")
    platform: PaymentPlatform = Field(..., description="Payment platform used")
    amount: int = Field(..., description="Amount paid in cents")
    currency: str = Field(..., description="Currency of the payment")
    status: PaymentStatus = Field(..., description="Current status of the payment")
    subscription_id: UUID4 = Field(..., description="ID of the user subscription related to this payment")
    stripe_payment_id: Optional[str] = Field(None, description="Stripe payment ID, if applicable")
    google_payment_id: Optional[str] = Field(None, description="Google payment ID, if applicable")
    apple_payment_id: Optional[str] = Field(None, description="Apple payment ID, if applicable")
    timestamp: datetime = Field(..., description="Timestamp of the payment")
    renewal_date: Optional[datetime] = Field(None, description="Date of subscription renewal")

    class Config:
        from_attributes = True


# Subscription Details Schema
class SubscriptionDetails(BaseModel):
    id: UUID4 = Field(..., description="ID of the user subscription")
    user_id: UUID4 = Field(..., description="ID of the user who owns the subscription")
    status: str = Field(..., description="Current status of the subscription")
    start_date: datetime = Field(..., description="Start date of the subscription")
    end_date: Optional[datetime] = Field(None, description="End date of the subscription")
    renewal_date: Optional[datetime] = Field(None, description="Next renewal date of the subscription")

    class Config:
        from_attributes = True
