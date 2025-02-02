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

### **Generate MFA Secret**
def generate_mfa_secret(email: str):
    """
    Generates a TOTP secret and QR code for MFA setup.
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
        logger.error(f"Error generating MFA secret for email {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate MFA secret")

### **Verify MFA Code**
def verify_mfa_code(secret: str, code: str) -> bool:
    """
    Verifies the provided TOTP code using the secret.
    """
    logger.info("Verifying MFA code")
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    except Exception as e:
        logger.error(f"Error verifying MFA code: {str(e)}")
        return False

### **Reset MFA for a User**
def reset_mfa(user_id: str, db: Session):
    """
    Reset the MFA configuration for a user.
    Clears the MFA secret and backup codes from the user.
    """
    logger.info(f"Resetting MFA for user_id: {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Clear MFA details
        user.mfa_secret = None
        user.mfa_backup_codes = None
        user.mfa_enabled = False
        db.commit()

        logger.info(f"MFA reset successfully for user_id: {user_id}")
    except SQLAlchemyError as e:
        logger.error(f"Database error while resetting MFA for user_id {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to reset MFA")
