from uuid import uuid4
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from datetime import datetime
from backend.api.payments.payment_routes import router
from backend.main import app
from backend.models.user import User, UserType
from backend.models.payment import Payment, PaymentPlatform, PaymentStatus
from backend.models.subscription_tier import SubscriptionTier

# Add the router to the test app
app.include_router(router)
client = TestClient(app)


# Fixture to create a mock user
@pytest.fixture
def mock_user(db_session):
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
def mock_subscription_tier(db_session):
    tier = SubscriptionTier(
        id=uuid4(),
        name="Pro",
        price=1999,
        currency="USD",
        is_active=True,
        recurring_interval="monthly",
        features=["Access to workouts", "Community posts"],
        version=1,
    )
    db_session.add(tier)
    db_session.commit()
    return tier


# Fixture to create a mock payment
@pytest.fixture
def mock_payment(db_session, mock_user, mock_subscription_tier):
    payment = Payment(
        id=uuid4(),
        user_id=mock_user.id,
        subscription_tier_id=mock_subscription_tier.id,
        stripe_payment_id="stripe-session-id",
        amount=1999,
        currency="USD",
        platform=PaymentPlatform.STRIPE,
        status=PaymentStatus.PENDING,
        timestamp=datetime.utcnow(),
    )
    db_session.add(payment)
    db_session.commit()
    return payment


# Test creating a payment
@patch("backend.api.payments.payment_service.create_stripe_payment")
def test_create_payment(mock_create_stripe_payment, mock_user, mock_subscription_tier, db_session):
    mock_create_stripe_payment.return_value = {"session_id": "session-id", "url": "https://stripe.com"}

    with patch("backend.api.payments.payment_routes.get_current_user", return_value=mock_user):
        response = client.post(f"/api/payments/create?subscription_tier={mock_subscription_tier.id}")
        assert response.status_code == 200
        assert response.json()["url"] == "https://stripe.com"


# Test verifying a payment
@patch("stripe.checkout.Session.retrieve")
def test_verify_payment(mock_retrieve_session, mock_user, mock_payment, db_session):
    mock_retrieve_session.return_value = {"payment_status": "paid"}

    with patch("backend.api.payments.payment_routes.get_current_user", return_value=mock_user):
        response = client.post(f"/api/payments/verify?session_id={mock_payment.stripe_payment_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Payment successful!"


# Test refunding a payment
@patch("stripe.Refund.create")
def test_refund_payment(mock_refund_create, mock_payment, mock_user, db_session):
    mock_refund_create.return_value = {"id": "refund-id"}

    with patch("backend.api.payments.payment_routes.get_current_user", return_value=mock_user):
        response = client.post(f"/api/payments/refund?payment_id={mock_payment.id}")
        assert response.status_code == 200
        assert response.json()["status"] == "FAILED"  # Refunded payments are marked as failed.


# Test fetching payment history
@patch("backend.api.payments.payment_service.get_user_payments")
def test_get_user_payment_history(mock_get_user_payments, mock_user, db_session):
    mock_get_user_payments.return_value = {
        "payments": [{"id": "payment-id-123", "amount": 1999}],
        "total_amount_spent": 1999,
    }

    with patch("backend.api.payments.payment_routes.get_current_user", return_value=mock_user):
        response = client.get("/api/payments/history?page=1&page_size=10")
        assert response.status_code == 200
        assert len(response.json()["payments"]) == 1
        assert response.json()["total_amount_spent"] == 1999


# Test handling invalid subscription tier during payment creation
def test_create_payment_invalid_subscription_tier(mock_user, db_session):
    with patch("backend.api.payments.payment_routes.get_current_user", return_value=mock_user):
        response = client.post("/api/payments/create?subscription_tier=invalid-tier-id")
        assert response.status_code == 400
        assert "Invalid subscription tier selected." in response.json()["detail"]
