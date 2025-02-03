import pyotp
import qrcode
from io import BytesIO
import base64
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend.models.user import User
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

def generate_mfa_secret(email: str):
    """
    Generates a TOTP secret and QR code for MFA setup.
    :param email: The email of the user for whom MFA is being set up.
    :return: A dictionary containing the secret, QR code URL, and manual key.
    """
    logger.info(f"Generating MFA secret for email: {email}")
    try:
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(name=email, issuer_name="Yoked App")

        # Generate QR Code
        qr_code_img = qrcode.make(provisioning_uri)
        buffer = BytesIO()
        qr_code_img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "mfa_secret": secret,
            "qr_code": f"data:image/png;base64,{qr_code_base64}",
            "manual_key": secret
        }
    except Exception as e:
        logger.error(f"Error generating MFA secret for email: {email}, error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate MFA secret")


def verify_mfa_code(secret: str, code: str) -> bool:
    """
    Verifies the provided TOTP code using the secret.
    :param secret: The TOTP secret used to generate codes.
    :param code: The TOTP code provided by the user.
    :return: True if the code is valid, False otherwise.
    """
    logger.info("Verifying MFA code")
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    except Exception as e:
        logger.error(f"Error verifying MFA code, error: {str(e)}")
        return False


def reset_mfa(user_id: str, db: Session):
    """
    Reset the MFA configuration for a user.
    Clears the MFA secret and backup codes from the user.
    """
    logger.info(f"Resetting MFA for user_id: {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User not found for MFA reset: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        # Clear MFA details
        user.mfa_secret = None
        user.mfa_backup_codes = None
        user.mfa_enabled = False
        db.commit()

        logger.info(f"MFA reset successfully for user_id: {user_id}")
    except SQLAlchemyError as e:
        logger.error(f"Database error while resetting MFA for user_id: {user_id}, error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to reset MFA")
