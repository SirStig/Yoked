from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.session_service import validate_session
from backend.models.session import SessionModel
from backend.core.logging_config import get_logger

logger = get_logger(__name__)

EXCLUDED_ROUTES = [
    "/api/auth/login",
    "/api/auth/register",
    "/api/auth/reset-password",
    "/api/auth/verify-email",
    "/api/users/profile",
    "/api/auth/logout",
    "/api/auth/resend-verification",
    "/api/payments/create",
    "/api/payments/cancel",
    "/api/payments/subscribe/free",
    "/api/payments/verify",
    "/api/subscriptions/",
    "/api/user/profile/version",
    "/api/subscriptions/version",
    "/api/admin/create",
    "/api/admin/login",
    "/api/admin/mfa/setup",
    "/api/admin/mfa/verify",
    "/api/settings/profile",
    "/api/settings/email",
    "/api/settings/password",
    "/api/settings/mfa",
    "/api/settings/sessions",
    "/api/settings/subscription",
    "/api/settings/notifications",
    "/api/settings/privacy",
    "/api/settings/reels",
    "/api/settings/community",
    "/api/settings/nutrition",
    "/api/settings/workout",
    "/api/settings/account",
]

class MFAMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Processing request to: {request.url.path}")

        # Skip middleware for excluded routes
        if any(request.url.path.startswith(route) for route in EXCLUDED_ROUTES):
            logger.debug(f"Skipping MFA check for route: {request.url.path}")
            return await call_next(request)

        # Extract session token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing or malformed Authorization header")
            return JSONResponse({"detail": "Authorization header is required"}, status_code=401)

        token = auth_header.split(" ")[1]

        # Validate session and check MFA
        db = next(get_db())
        try:
            session: SessionModel = validate_session(token, db)
            if not session.mfa_verified:
                logger.warning(f"MFA not verified for session: {session.id}")
                return JSONResponse({"detail": "MFA verification required"}, status_code=403)
            logger.info(f"Session {session.id} passed MFA verification")
        except HTTPException as e:
            logger.error(f"MFA validation failed: {str(e)}")
            return JSONResponse({"detail": f"MFA validation failed: {e.detail}"}, status_code=403)
        except Exception as e:
            logger.error(f"Unexpected error in MFA middleware: {str(e)}")
            return JSONResponse({"detail": "Unexpected error in middleware"}, status_code=500)
        finally:
            db.close()

        return await call_next(request)
