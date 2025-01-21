from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from backend.services.session_service import validate_session
from backend.core.database import get_db
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)


class SessionValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow OPTIONS requests to pass through
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
        ]

        # Check if the route is in the list of public routes
        if any(request.url.path.startswith(route) for route in PUBLIC_ROUTES):
            return await call_next(request)

        # Proceed with session validation for other routes
        if request.url.path.startswith("/api/") and "auth" not in request.url.path:
            try:
                # Retrieve the Authorization header
                auth_header = request.headers.get("Authorization")
                logger.debug(f"Authorization Header: {auth_header}")

                if auth_header and auth_header.startswith("Bearer "):
                    # Extract the token from the header
                    token = auth_header.split(" ")[1]
                    logger.debug(f"Extracted Token: {token}")

                    # Manually retrieve a database session from the generator
                    db = next(get_db())
                    try:
                        validate_session(token, db)  # Validate the session token
                    finally:
                        db.close()  # Ensure the database session is closed
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

