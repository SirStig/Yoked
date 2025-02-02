from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.core.database import get_db
from backend.core.logging_config import get_logger
from backend.schemas.user_schema import UserCreate, LoginRequest, UserMFASetup, UserMFAVerify
from backend.services.mfa import generate_mfa_secret, verify_mfa_code
from backend.api.admin.admin_service import create_admin_user, list_admin_users, moderate_flagged_users
from backend.models.user import User, UserType
from backend.api.auth.auth_service import verify_password
from backend.services.session_service import create_session, validate_session

router = APIRouter()
logger = get_logger(__name__)


@router.post("/create", tags=["Admin"])
def create_admin(
        user_data: UserCreate,
        x_superuser_secret: str = Header(None),
        db: Session = Depends(get_db),
):
    """ Securely create a new admin user. """
    try:
        if x_superuser_secret != settings.SUPERUSER_CREATION_SECRET_KEY:
            logger.warning("Invalid secret key attempt for admin creation")
            raise HTTPException(status_code=403, detail="Invalid secret key. Access denied.")

        new_admin = create_admin_user(db, user_data)
        logger.info(f"Admin user created: {new_admin.username}")
        return {"message": f"Admin user {new_admin.username} created successfully"}

    except HTTPException as e:
        logger.error(f"Admin creation failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during admin creation")
        raise HTTPException(status_code=500, detail="Failed to create admin user")


@router.post("/login", tags=["Admin"])
async def admin_login(user_data: LoginRequest, db: Session = Depends(get_db)):
    """ Login an admin and enforce MFA requirements. """
    try:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if user.user_type != UserType.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied")

        if user.admin_secret_key != settings.SUPERUSER_CREATION_SECRET_KEY:
            raise HTTPException(status_code=403, detail="Access denied")

        if user.flagged_for_review:
            raise HTTPException(status_code=403, detail="Account under review")

        session_token = create_session(user.id, db, is_mobile=user_data.is_mobile)

        if not user.mfa_secret:
            return {"mfa_setup_required": True, "user_id": user.id, "session_token": session_token}

        if user.mfa_enabled:
            return {"mfa_required": True, "user_id": user.id, "session_token": session_token}

        return {"success": True, "session_token": session_token}

    except HTTPException as e:
        logger.error(f"Admin login failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error during admin login")
        raise HTTPException(status_code=500, detail="Login failed. Please try again.")


@router.get("/mfa/setup", tags=["Admin"])
def get_mfa_setup(user_id: UUID, db: Session = Depends(get_db)):
    """ Generate a QR code and manual key for MFA setup. """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.user_type != UserType.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied")

        if user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA is already set up")

        mfa_data = generate_mfa_secret(user.email)
        return {"qr_code_url": mfa_data["qr_code"], "manual_key": mfa_data["manual_key"]}

    except HTTPException as e:
        logger.error(f"MFA setup failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error in MFA setup")
        raise HTTPException(status_code=500, detail="Failed to generate MFA setup")


@router.post("/mfa/setup", tags=["Admin"])
def post_mfa_setup(data: UserMFASetup, db: Session = Depends(get_db)):
    """ Verify the TOTP code, enable MFA, and return a session token. """
    try:
        user = db.query(User).filter(User.id == data.user_id).first()

        if not user or user.user_type != UserType.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied")

        if not verify_mfa_code(data.mfa_secret, data.totp_code):
            raise HTTPException(status_code=400, detail="Invalid TOTP code")

        user.mfa_secret = data.mfa_secret
        user.mfa_enabled = True
        db.commit()

        session_token = create_session(user.id, db, is_mobile=False)

        logger.info(f"MFA setup successful for admin: {user.id}")
        return {"session_token": session_token}

    except HTTPException as e:
        logger.error(f"MFA setup failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error in MFA setup")
        raise HTTPException(status_code=500, detail="Failed to enable MFA")


@router.post("/mfa/verify", tags=["Admin"])
def post_mfa_verify(data: UserMFAVerify, db: Session = Depends(get_db)):
    """ Verify the TOTP code for login or protected access and return a session token. """
    try:
        session = validate_session(data.session_token, db)

        user = db.query(User).filter(User.id == session.user_id).first()
        if not user or user.user_type != UserType.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied")

        if not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA is not set up for this user")

        if not verify_mfa_code(user.mfa_secret, data.totp_code):
            raise HTTPException(status_code=400, detail="Invalid TOTP code")

        session.mfa_verified = True
        db.commit()

        logger.info(f"MFA verified successfully for user: {user.id}")
        return {"message": "MFA verification successful", "session_token": session.token}

    except HTTPException as e:
        logger.error(f"MFA verification failed: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unexpected error in MFA verification")
        raise HTTPException(status_code=500, detail="MFA verification failed")


@router.get("/list", tags=["Admin"])
def list_admins(db: Session = Depends(get_db)):
    """ List all admin users. """
    try:
        return list_admin_users(db)
    except Exception as e:
        logger.exception("Error fetching admin users")
        raise HTTPException(status_code=500, detail="Failed to retrieve admin users")


@router.get("/moderate-flagged", tags=["Admin"])
def moderate_users(db: Session = Depends(get_db)):
    """ List all users flagged for review. """
    try:
        return moderate_flagged_users(db)
    except Exception as e:
        logger.exception("Error retrieving flagged users")
        raise HTTPException(status_code=500, detail="Failed to retrieve flagged users")
