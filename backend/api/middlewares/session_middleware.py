from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from backend.services.session_service import validate_session
from backend.core.database import get_db
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

class SessionValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        """ Middleware for session validation and tracking. """
        if request.method == "OPTIONS":
            return await call_next(request)

        PUBLIC_ROUTES = [
            "/api/auth/login",
            "/api/auth/register",
            "/api/auth/reset-password",
            "/api/auth/verify-email",
            "/api/subscriptions/",
            "/api/user/profile/version",
            "/api/subscriptions/version",
            "/api/admin/create",
            "/api/admin/login",
            "/api/admin/mfa/setup",
            "/api/admin/mfa/verify",
        ]

        logger.debug(f"Processing request to: {request.url.path}")

        if any(request.url.path.startswith(route) for route in PUBLIC_ROUTES):
            return await call_next(request)

        if request.url.path.startswith("/api/") and "auth" not in request.url.path:
            try:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

                    db = next(get_db())
                    try:
                        session = validate_session(token, db)
                        if not session.is_active:
                            logger.warning(f"Inactive session: {session.id}")
                            return JSONResponse({"detail": "Session is inactive"}, status_code=401)

                        # Update last activity timestamp
                        session.last_activity = datetime.utcnow()
                        db.commit()

                        request.state.session = session
                    finally:
                        db.close()
                else:
                    return JSONResponse(
                        {"detail": "Unauthorized: Missing or invalid token"},
                        status_code=401,
                    )
            except Exception as e:
                logger.error(f"Session validation error: {str(e)}")
                return JSONResponse(
                    {"detail": f"Unauthorized: {str(e)}"},
                    status_code=401,
                )

        return await call_next(request)
