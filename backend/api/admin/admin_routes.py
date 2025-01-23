from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.core.database import get_db
from backend.core.logging_config import get_logger
from backend.schemas.user_schema import UserCreate, LoginRequest, UserMFASetup, UserMFAVerify
from backend.services.mfa import generate_mfa_secret, verify_mfa_code
from backend.api.admin.admin_service import create_admin_user, list_admin_users, moderate_flagged_users
from backend.models.user import User
from backend.api.auth.auth_service import verify_password
from backend.services.session_service import create_session

router = APIRouter()

logger = get_logger(__name__)

@router.post("/create", tags=["Admin"])
def create_admin(
    user_data: UserCreate,
    x_superuser_secret: str = Header(None),
    db: Session = Depends(get_db),
):
    """
    Securely create a new admin user.
    """
    user_data.admin_secret_key = x_superuser_secret
    logger.debug(f"Received user_data: {user_data}")
    try:
        valid_secret_key = settings.SUPERUSER_CREATION_SECRET_KEY
        if x_superuser_secret != valid_secret_key:
            raise HTTPException(
                status_code=403,
                detail="Invalid secret key. Access denied."
            )

        # Create the admin user
        new_admin = create_admin_user(db, user_data)
        return {"message": f"Admin user {new_admin.username} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create admin user")


@router.post("/login", tags=["Admin"])
async def admin_login(user_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login an admin and enforce MFA requirements (setup or verification).
    """
    logger.debug(f"Attempting to log in admin: {user_data.email}")
    try:
        # Fetch the user
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            logger.warning(f"Invalid login attempt for email: {user_data.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Ensure the user is an admin
        if user.user_type != "ADMIN":
            logger.warning(f"Unauthorized login attempt by non-admin user: {user.id}")
            raise HTTPException(status_code=403, detail="Access denied")

        # Enforce MFA setup or verification
        if not user.mfa_secret:
            logger.info(f"MFA setup required for admin: {user.id}")
            return {"mfa_setup_required": True, "user_id": user.id}

        if user.mfa_enabled:
            logger.info(f"MFA verification required for admin: {user.id}")
            session_token = create_session(user.id, db, is_mobile=user_data.is_mobile)
            return {"mfa_required": True, "session_token": session_token}

        # Create a session if no MFA is required
        session_token = create_session(user.id, db, is_mobile=user_data.is_mobile)
        logger.info(f"Admin {user.id} logged in successfully.")
        return {"success": True, "session_token": session_token}

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/mfa/setup", tags=["Admin"])
def get_mfa_setup(user_id: int, db: Session = Depends(get_db)):
    """
    Generate a QR code and manual key for MFA setup.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    if user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA is already set up")

    mfa_data = generate_mfa_secret(user.email)
    return {"qr_code_url": mfa_data["qr_code"], "manual_key": mfa_data["manual_key"]}


@router.post("/mfa/setup", tags=["Admin"])
def post_mfa_setup(data: UserMFASetup, db: Session = Depends(get_db)):
    """
    Verify the provided TOTP code and enable MFA.
    """
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    if not verify_mfa_code(data.mfa_secret, data.totp_code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")

    user.mfa_secret = data.mfa_secret
    user.mfa_enabled = True
    db.commit()

    return {"message": "MFA setup successfully"}


@router.post("/mfa/verify", tags=["Admin"])
def post_mfa_verify(data: UserMFAVerify, db: Session = Depends(get_db)):
    """
    Verify the TOTP code for login or protected access.
    """
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    if not user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA is not set up for this user")

    if not verify_mfa_code(user.mfa_secret, data.totp_code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")

    return {"message": "MFA verification successful"}


@router.get("/list", tags=["Admin"])
def list_admins(db: Session = Depends(get_db)):
    """
    List all admin users.
    """
    return list_admin_users(db)


@router.get("/moderate-flagged", tags=["Admin"])
def moderate_users(db: Session = Depends(get_db)):
    """
    List all users flagged for review.
    """
    return moderate_flagged_users(db)
