from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List
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
    PAID = "paid"
    COMPLETE = "complete"


# Base Subscription Tier Schema
class SubscriptionTierBase(BaseModel):
    name: str = Field(..., description="Name of the subscription tier")
    description: Optional[str] = Field(default=None, description="Description of the subscription tier")
    price: int = Field(..., description="Price in cents for the subscription")
    currency: str = Field(..., description="Currency of the subscription price")
    features: Optional[List[str]] = Field(
        default=None, description="List of features included in the subscription tier"
    )
    is_active: bool = Field(..., description="Whether the tier is currently active and available")
    has_ads: bool = Field(..., description="Indicates if the subscription includes ads")
    access_reels: bool = Field(..., description="Access to 'Yoked Reels'")
    reels_ad_free: bool = Field(..., description="Ad-free experience for reels")
    access_workouts: bool = Field(..., description="Access to workout videos and routines")
    workout_filters: bool = Field(..., description="Availability of advanced workout filters")
    access_community_read: bool = Field(..., description="Read-only access to community forums")
    access_community_post: bool = Field(..., description="Permission to post in community forums")
    private_community_challenges: bool = Field(..., description="Access to private community challenges")
    access_nutrition: bool = Field(..., description="Access to nutrition articles and recipes")
    calorie_tracking: bool = Field(..., description="Access to calorie tracking tools")
    personalized_nutrition: bool = Field(..., description="Availability of personalized nutrition plans")
    direct_messaging: bool = Field(..., description="Direct messaging capabilities")
    basic_progress_tracking: bool = Field(..., description="Basic progress tracking features")
    enhanced_progress_tracking: bool = Field(..., description="Enhanced progress tracking tools")
    access_live_classes: bool = Field(..., description="Access to live fitness classes")
    one_on_one_coaching: bool = Field(..., description="One-on-one coaching availability")
    priority_support: bool = Field(..., description="Priority support from the Yoked team")
    is_trial_available: bool = Field(..., description="Indicates if a trial period is available")
    trial_period_days: int = Field(..., description="Length of the trial period in days")
    billing_cycle: str = Field(..., description="Billing cycle for the subscription (e.g., monthly, yearly)")
    cancellation_policy: str = Field(..., description="Details of the subscription's cancellation policy")
    max_reel_uploads: int = Field(..., description="Maximum number of reel uploads allowed")
    max_saved_workouts: int = Field(..., description="Maximum number of saved workouts allowed")
    max_messages_per_day: int = Field(..., description="Maximum number of messages allowed per day")
    recurring_interval: str = Field(..., description="Recurring interval for the subscription")
    version: int = Field(..., description="Version of the subscription tier")  # Added field

    class Config:
        orm_mode = True


# Output Schema for Subscription Tier
class SubscriptionTierOut(BaseModel):
    id: UUID = Field(..., description="Unique identifier for the subscription tier")
    name: str = Field(..., description="Name of the subscription tier")
    description: Optional[str] = Field(None, description="Description of the subscription tier")
    price: int = Field(..., description="Price in cents for the subscription")
    currency: str = Field(..., description="Currency of the subscription price")
    features: List[str] = Field(..., description="List of features included in the subscription tier")
    is_active: bool = Field(..., description="Whether the tier is currently active and available")
    has_ads: bool = Field(..., description="Indicates if the tier includes advertisements")
    reels_ad_free: bool = Field(..., description="Whether the tier offers ad-free reels")
    access_workouts: bool = Field(..., description="Whether the tier includes workout access")
    workout_filters: bool = Field(..., description="Whether the tier includes workout filters")
    access_community_read: bool = Field(..., description="Read-only access to community forums")
    access_community_post: bool = Field(..., description="Posting access to community forums")
    private_community_challenges: bool = Field(..., description="Access to private community challenges")
    access_nutrition: bool = Field(..., description="Access to general nutrition articles")
    calorie_tracking: bool = Field(..., description="Access to calorie tracking tools")
    personalized_nutrition: bool = Field(..., description="Access to personalized nutrition plans")
    direct_messaging: bool = Field(..., description="Access to direct messaging with members")
    basic_progress_tracking: bool = Field(..., description="Access to basic progress tracking tools")
    enhanced_progress_tracking: bool = Field(..., description="Access to enhanced progress tracking tools")
    access_live_classes: bool = Field(..., description="Access to live fitness classes")
    one_on_one_coaching: bool = Field(..., description="Access to one-on-one coaching")
    priority_support: bool = Field(..., description="Access to priority support")
    is_hidden: bool = Field(..., description="Indicates if the tier is hidden")
    is_trial_available: bool = Field(..., description="Whether a trial is available for the tier")
    trial_period_days: int = Field(..., description="Number of days for the trial period")
    billing_cycle: str = Field(..., description="Billing cycle for the subscription tier")
    cancellation_policy: str = Field(..., description="Cancellation policy for the subscription tier")
    max_reel_uploads: int = Field(..., description="Maximum number of reel uploads")
    max_saved_workouts: int = Field(..., description="Maximum number of saved workouts")
    max_messages_per_day: int = Field(..., description="Maximum number of messages per day")
    recurring_interval: str = Field(..., description="Recurring interval for the subscription")
    version: int = Field(..., description="Version of the subscription tier")  # Added field

    class Config:
        orm_mode = True



# Payment Create Schema
class PaymentCreate(BaseModel):
    user_id: Optional[UUID] = Field(None, description="The UUID of the user making the payment")
    platform: PaymentPlatform = Field(..., description="Payment platform used")
    amount: int = Field(..., description="Amount paid in cents")
    currency: str = Field(..., description="Currency of the payment")
    subscription_tier_id: UUID = Field(..., description="ID of the subscription tier being purchased")
    stripe_payment_id: Optional[str] = Field(None, description="Stripe payment ID, if applicable")
    google_payment_id: Optional[str] = Field(None, description="Google payment ID, if applicable")
    apple_payment_id: Optional[str] = Field(None, description="Apple payment ID, if applicable")
    renewal_date: Optional[datetime] = Field(None, description="Date of subscription renewal")

    class Config:
        orm_mode = True


# Payment Output Schema
class PaymentOut(BaseModel):
    id: UUID = Field(..., description="Unique payment ID")
    user_id: UUID = Field(..., description="The UUID of the user who made the payment")
    platform: PaymentPlatform = Field(..., description="Payment platform used")
    amount: int = Field(..., description="Amount paid in cents")
    currency: str = Field(..., description="Currency of the payment")
    status: PaymentStatus = Field(..., description="Current status of the payment")
    subscription_tier: SubscriptionTierOut = Field(..., description="Details of the subscription tier purchased")
    stripe_payment_id: Optional[str] = Field(None, description="Stripe payment ID, if applicable")
    google_payment_id: Optional[str] = Field(None, description="Google payment ID, if applicable")
    apple_payment_id: Optional[str] = Field(None, description="Apple payment ID, if applicable")
    timestamp: datetime = Field(..., description="Timestamp of the payment")
    renewal_date: Optional[datetime] = Field(None, description="Date of subscription renewal")

    class Config:
        orm_mode = True


# Payment Verification Schema
class PaymentVerify(BaseModel):
    payment_id: UUID = Field(..., description="The payment ID to verify")
    platform: PaymentPlatform = Field(..., description="Payment platform for verification")
    verification_token: Optional[str] = Field(None, description="Token or identifier to verify the payment")

    class Config:
        orm_mode = True


# User Payment History Schema
class PaymentHistory(BaseModel):
    payments: List[PaymentOut] = Field(..., description="List of payments for the user")
    total_amount_spent: Optional[int] = Field(0, description="Total amount spent by the user in cents")

    class Config:
        orm_mode = True


# Admin Payment History Schema
class AdminPaymentHistory(BaseModel):
    user_id: UUID = Field(..., description="UUID of the user")
    user_email: str = Field(..., description="Email of the user")
    payments: List[PaymentOut] = Field(..., description="List of payments made by the user")
    total_amount_spent: Optional[int] = Field(0, description="Total amount spent by the user in cents")

    class Config:
        orm_mode = True
