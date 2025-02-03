from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header
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
        if user.user_type != UserType.ADMIN:
            logger.warning(f"Unauthorized login attempt by non-admin user: {user.id}")
            raise HTTPException(status_code=403, detail="Access denied")

        #Verify Admin_Secret
        if user.admin_secret_key != settings.SUPERUSER_CREATION_SECRET_KEY:
            logger.warning(f"Invalid Admin Secret Key for User: {user.id}")
            raise HTTPException(status_code=403, detail="Access denied")

        #Verify Account Flag
        if user.flagged_for_review:
            logger.warning(f"User {user.id} has been flagged for review")
            raise HTTPException(status_code=403, detail="Access denied")


        session_token = create_session(user.id, db, is_mobile=user_data.is_mobile)
        # Enforce MFA setup or verification
        if not user.mfa_secret:
            logger.info(f"MFA setup required for admin: {user.id}")
            return {"mfa_setup_required": True, "user_id": user.id, "session_token": session_token}

        if user.mfa_enabled:
            logger.info(f"MFA verification required for admin: {user.id}")
            return {"mfa_required": True, "user_id": user.id, "session_token": session_token}

        logger.info(f"Admin {user.id} logged in successfully.")
        return {"success": True, "session_token": session_token}

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


from fastapi import Query

@router.get("/mfa/setup", tags=["Admin"])
def get_mfa_setup(user_id: str = Query(..., description="User ID for MFA setup"), db: Session = Depends(get_db)):
    """
    Generate a QR code and manual key for MFA setup.
    """
    # Fetch the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")

    # Check if MFA is already set up
    if user.mfa_secret:
        raise HTTPException(status_code=400, detail="MFA is already set up")

    # Generate MFA secret and QR code
    mfa_data = generate_mfa_secret(user.email)
    return {"qr_code_url": mfa_data["qr_code"], "manual_key": mfa_data["manual_key"]}



@router.post("/mfa/setup", tags=["Admin"])
def post_mfa_setup(data: UserMFASetup, db: Session = Depends(get_db)):
    """
    Verify the provided TOTP code, enable MFA, and return a session token.
    """
    user_id = str(data.user_id)
    user = db.query(User).filter(User.id == user_id).first()

    if not user or user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")

    if not verify_mfa_code(data.mfa_secret, data.totp_code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")

    # Enable MFA
    user.mfa_secret = data.mfa_secret
    user.mfa_enabled = True
    db.commit()

    # Create session token
    session_token = create_session(user.id, db, is_mobile=False)

    logger.info(f"MFA setup successful for admin: {user.id}")
    return {"session_token": session_token}


@router.post("/mfa/verify", tags=["Admin"])
def post_mfa_verify(data: UserMFAVerify, db: Session = Depends(get_db)):
    """
    Verify the TOTP code for login or protected access and return a session token.
    """
    logger.debug(f"User MFA verify: user_id={data.user_id}, totp_code={data.totp_code}")
    try:
        # Validate the session and retrieve the user
        session = validate_session(data.session_token, db)

        # Validate user details
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user or user.user_type != UserType.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied")

        if not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA is not set up for this user")

        # Verify the provided TOTP code
        if not verify_mfa_code(user.mfa_secret, data.totp_code):
            raise HTTPException(status_code=400, detail="Invalid TOTP code")

        # Mark the session as MFA verified
        session.mfa_verified = True
        db.commit()

        logger.info(f"MFA verified successfully for user: {user.id}")
        return {"message": "MFA verification successful", "session_token": session.token}

    except HTTPException as e:
        logger.error(f"MFA verification error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in /mfa/verify: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")




@router.get("/profile", tags=["Admin"])
def get_admin_profile(db: Session = Depends(get_db), token: str = Depends(settings.oauth2_scheme)):
    """
    Fetch the current admin's profile.
    """
    logger.debug(f"Received /profile request with token: {token}")
    try:
        # Validate the token and retrieve the session
        session = validate_session(token, db)
        if not session:
            logger.warning("Invalid session or token")
            raise HTTPException(status_code=401, detail="Invalid session")

        # Fetch the user from the database using the session's user_id
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user or user.user_type != UserType.ADMIN:
            logger.warning(f"Unauthorized access attempt or invalid user type: {user}")
            raise HTTPException(status_code=403, detail="Access denied")

        logger.info(f"Fetched profile for admin user: {user.email}")
        return {"user_type": user.user_type, "email": user.email, "full_name": user.full_name}
    except Exception as e:
        logger.error(f"Error in /profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")



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
