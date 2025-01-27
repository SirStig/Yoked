from uuid import uuid4
import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.models.subscription_tier import SubscriptionTier
from backend.models.user import User, UserType
from backend.models.payment import Payment, PaymentStatus, PaymentPlatform
from backend.schemas.payment_schema import UpdateSubscription
from backend.api.subscriptions.subscription_service import (
    get_user_subscription_details,
    update_user_subscription,
    cancel_user_subscription,
)


# Fixture: Create a mock user
@pytest.fixture
def mock_user(db_session: Session):
    user = User(
        id=uuid4(),
        full_name="Test User",
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashed_password",
        is_active=True,
        is_verified=True,
        user_type=UserType.REGULAR,
        subscription_plan="Free",
        accepted_terms=True,
        accepted_privacy_policy=True,
        accepted_terms_at=datetime.utcnow(),
        accepted_privacy_policy_at=datetime.utcnow(),
    )
    db_session.add(user)
    db_session.commit()
    return user


# Fixture: Create a mock subscription tier
@pytest.fixture
def mock_subscription_tier(db_session: Session):
    tier = SubscriptionTier(
        id=uuid4(),
        name="Pro",
        price=1999,
        currency="USD",
        recurring_interval="monthly",
        is_active=True,
        features=["Access to workouts", "Ad-free experience"],
        version=1,
    )
    db_session.add(tier)
    db_session.commit()
    return tier


# Fixture: Create a mock payment
@pytest.fixture
def mock_payment(db_session: Session, mock_user, mock_subscription_tier):
    payment = Payment(
        id=uuid4(),
        user_id=mock_user.id,
        subscription_tier_id=mock_subscription_tier.id,
        platform=PaymentPlatform.STRIPE,
        status=PaymentStatus.SUCCESS,
        amount=1999,
        currency="USD",
        renewal_date=datetime.utcnow() + timedelta(days=30),
        timestamp=datetime.utcnow(),
    )
    db_session.add(payment)
    db_session.commit()
    return payment


# Test: Get User Subscription Details
def test_get_user_subscription_details(mock_user, mock_payment, db_session):
    subscription_details = get_user_subscription_details(mock_user.id, db_session)

    assert subscription_details.subscription_name == "Pro"
    assert subscription_details.price == 1999
    assert subscription_details.currency == "USD"
    assert subscription_details.status == "Active"
    assert subscription_details.renewal_date is not None


# Test: Update User Subscription
@patch("stripe.Subscription.modify")
def test_update_user_subscription(mock_stripe_modify, mock_user, mock_subscription_tier, db_session):
    mock_stripe_modify.return_value = {"current_period_end": 1700000000}  # Mock Stripe response

    subscription_data = UpdateSubscription(subscription_tier_id=mock_subscription_tier.id)
    update_user_subscription(mock_user.id, subscription_data, db_session)

    updated_user = db_session.query(User).filter_by(id=mock_user.id).first()
    updated_payment = db_session.query(Payment).filter_by(user_id=mock_user.id).first()

    assert updated_user.subscription_plan == mock_subscription_tier.name
    assert updated_payment.subscription_tier_id == mock_subscription_tier.id
    assert updated_payment.renewal_date is not None


# Test: Cancel User Subscription
@patch("stripe.Subscription.delete")
def test_cancel_user_subscription(mock_stripe_delete, mock_user, mock_payment, db_session):
    mock_stripe_delete.return_value = {"id": "sub-id-123", "status": "canceled"}  # Mock Stripe response

    cancel_user_subscription(mock_user.id, db_session)

    updated_user = db_session.query(User).filter_by(id=mock_user.id).first()
    updated_payment = db_session.query(Payment).filter_by(user_id=mock_user.id).first()

    assert updated_user.subscription_plan == "Free"
    assert updated_payment.status == PaymentStatus.CANCELED
    assert updated_payment.renewal_date is None