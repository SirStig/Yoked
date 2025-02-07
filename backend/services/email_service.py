import random
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from backend.models.user import User
from backend.core.config import settings
from backend.core.logging_config import get_logger
from backend.templates.email_templates import EMAIL_CODE_TEMPLATE

logger = get_logger(__name__)

# Expiration time for verification codes (10 minutes)
VERIFICATION_CODE_EXPIRY = timedelta(minutes=10)


def generate_verification_code(length=6):
    """
    Generate a random numeric verification code.
    """
    return ''.join(random.choices(string.digits, k=length))


async def send_verification_email(db: Session, user: User, email_type: str):
    """
    Sends a verification email containing a unique 6-digit code.

    Parameters:
        db (Session): Database session.
        user (User): User object.
        email_type (str): Purpose of the verification (e.g., "email_update", "password_reset").

    Returns:
        dict: Success message.
    """
    verification_code = generate_verification_code()

    # Store the verification code with expiration
    user.verification_code = verification_code
    user.verification_expires_at = datetime.utcnow() + VERIFICATION_CODE_EXPIRY
    db.commit()

    # Prepare email context
    email_context = {
        "username": user.full_name or user.email,
        "verification_code": verification_code,
        "current_year": datetime.utcnow().year
    }

    # Prepare and send email
    try:
        body = EMAIL_CODE_TEMPLATE.render(email_context)
        message = MessageSchema(
            subject="Your Verification Code",
            recipients=[user.email],
            body=body,
            subtype="html"
        )

        fm = FastMail(ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=settings.USE_CREDENTIALS,
        ))

        await fm.send_message(message)
        logger.info(f"Verification email sent to {user.email}")
        return {"message": f"Verification code sent to {user.email}"}

    except Exception as e:
        logger.error(f"Failed to send verification email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email.")
