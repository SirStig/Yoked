import pyotp
import qrcode
from io import BytesIO
import base64

def generate_mfa_secret(email: str):
    """
    Generates a TOTP secret and QR code for MFA setup.
    :param email: The email of the user for whom MFA is being set up.
    :return: A dictionary containing the secret, QR code URL, and manual key.
    """
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

def verify_mfa_code(secret: str, code: str) -> bool:
    """
    Verifies the provided TOTP code using the secret.
    :param secret: The TOTP secret used to generate codes.
    :param code: The TOTP code provided by the user.
    :return: True if the code is valid, False otherwise.
    """
    try:
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
    except Exception as e:
        return False
