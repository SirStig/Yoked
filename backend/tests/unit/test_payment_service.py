import pytest
from unittest.mock import patch
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from backend.api.payments.payment_service import (
    create_stripe_payment,
    create_payment,
    verify_payment,
    refund_payment,
    get_user_payments,
)
from backend.models.user import User, UserType
from backend.models.payment import Payment, PaymentPlatform, PaymentStatus
from backend.models.subscription_tier import SubscriptionTier
from backend.schemas.payment_schema import PaymentCreate, PaymentVerify


# Fixture to create a mock user
@pytest.fixture
def mock_user(db_session: Session):
    user = User(
        id=uuid4(),
        full_name="Test User",
        username="testuser",
        email="testuser@example.com",
        hashed_password="hashedpassword",
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


# Fixture to create a mock subscription tier
@pytest.fixture
def mock_subscription_tier(db_session: Session):
    tier = SubscriptionTier(
        id=uuid4(),
        name="Pro",
        price=1999,
        currency="USD",
        is_active=True,
        recurring_interval="monthly",
    )
    db_session.add(tier)
    db_session.commit()
    return tier


# Test creating a Stripe payment
@patch("stripe.checkout.Session.create")
def test_create_stripe_payment(mock_stripe_create, mock_user, mock_subscription_tier, db_session):
    mock_stripe_create.return_value = {"id": "session_test123", "url": "https://stripe.com"}

    payment_session = create_stripe_payment(mock_user, mock_subscription_tier.id, db_session)

    assert payment_session["session_id"] == "session_test123"
    assert payment_session["url"] == "https://stripe.com"


# Test creating a payment record
def test_create_payment(db_session: Session, mock_user, mock_subscription_tier):
    payment_data = PaymentCreate(
        user_id=mock_user.id,
        platform=PaymentPlatform.STRIPE,
        amount=mock_subscription_tier.price,
        currency=mock_subscription_tier.currency,
        subscription_tier_id=mock_subscription_tier.id,
        stripe_payment_id="stripe_test123",
    )

    payment = create_payment(db_session, payment_data, mock_user.id)

    assert payment.user_id == mock_user.id
    assert payment.platform == PaymentPlatform.STRIPE
    assert payment.amount == mock_subscription_tier.price
    assert payment.currency == mock_subscription_tier.currency
    assert payment.subscription_tier_id == mock_subscription_tier.id


# Test verifying a payment
@patch("stripe.PaymentIntent.retrieve")
def test_verify_payment(mock_stripe_retrieve, db_session: Session, mock_user, mock_subscription_tier):
    mock_stripe_retrieve.return_value = {"status": "succeeded"}

    payment = Payment(
        id=uuid4(),
        user_id=mock_user.id,
        subscription_tier_id=mock_subscription_tier.id,
        stripe_payment_id="stripe_test123",
        platform=PaymentPlatform.STRIPE,
        amount=1999,
        status=PaymentStatus.PENDING,
        timestamp=datetime.utcnow(),
    )
    db_session.add(payment)
    db_session.commit()

    payment_verify = PaymentVerify(payment_id=payment.id, platform=PaymentPlatform.STRIPE)

    verified_payment = verify_payment(db_session, payment_verify, mock_user.id)

    assert verified_payment.status == PaymentStatus.SUCCESS


# Test refunding a payment
@patch("stripe.Refund.create")
def test_refund_payment(mock_stripe_refund, db_session: Session, mock_user, mock_subscription_tier):
    mock_stripe_refund.return_value = {"id": "refund_test123"}

    payment = Payment(
        id=uuid4(),
        user_id=mock_user.id,
        subscription_tier_id=mock_subscription_tier.id,
        stripe_payment_id="stripe_test123",
        platform=PaymentPlatform.STRIPE,
        amount=1999,
        status=PaymentStatus.SUCCESS,
        timestamp=datetime.utcnow(),
    )
    db_session.add(payment)
    db_session.commit()

    refunded_payment = refund_payment(payment.id, db_session)

    assert refunded_payment.status == PaymentStatus.FAILED  # Refunded payments are marked as failed.


# Test fetching user payment history
def test_get_user_payments(db_session: Session, mock_user, mock_subscription_tier):
    for i in range(5):
        payment = Payment(
            id=uuid4(),
            user_id=mock_user.id,
            subscription_tier_id=mock_subscription_tier.id,
            stripe_payment_id=f"stripe_test{i}",
            platform=PaymentPlatform.STRIPE,
            amount=1999,
            status=PaymentStatus.SUCCESS,
            timestamp=datetime.utcnow(),
        )
        db_session.add(payment)
    db_session.commit()

    payment_history = get_user_payments(mock_user.id, page=1, page_size=2, db=db_session)

    assert len(payment_history.payments) == 2  # Paginated results
    assert payment_history.payments[0].amount == 1999
    assert payment_history.total_amount_spent == 5 * 1999