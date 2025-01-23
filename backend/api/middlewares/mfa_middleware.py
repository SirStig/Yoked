from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.session_service import validate_session
from backend.models.session import Session as SessionModel
from backend.core.logging_config import get_logger

logger = get_logger(__name__)

EXCLUDED_ROUTES = [
    "/api/admin/login",
    "/api/admin/register",
    "/api/admin/mfa/setup",
    "/api/admin/mfa/verify",
]

class MFAMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware to enforce MFA validation for protected admin routes.
        """
        logger.debug(f"Processing request to: {request.url.path}")

        # Skip middleware for excluded routes
        if any(request.url.path.startswith(route) for route in EXCLUDED_ROUTES):
            logger.debug(f"Skipping MFA check for route: {request.url.path}")
            return await call_next(request)

        # Extract session token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Missing or malformed Authorization header")
            return Response(content="Authorization header is required", status_code=401)

        token = auth_header.split(" ")[1]

        # Manually handle the database session
        db = next(get_db())
        try:
            # Validate session and ensure MFA is verified
            session: SessionModel = validate_session(token, db)
            if not session.mfa_verified:
                logger.warning(f"MFA not verified for session: {session.id}")
                return Response(content="MFA verification required", status_code=403)
            logger.info(f"Session {session.id} passed MFA verification")

            # Proceed to the next middleware or route
            return await call_next(request)

        except HTTPException as e:
            logger.error(f"MFA validation failed: {str(e)}")
            return Response(content=str(e.detail), status_code=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error in MFA middleware: {str(e)}")
            return Response(content="Unexpected error in middleware", status_code=500)
        finally:
            # Ensure the database session is closed
            db.close()
