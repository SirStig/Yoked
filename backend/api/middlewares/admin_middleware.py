from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from backend.core.config import settings
from backend.services.session_service import validate_session
from backend.core.database import get_db
from backend.core.logging_config import get_logger

# Logger setup
logger = get_logger(__name__)

class AdminValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow OPTIONS requests to pass through
        if request.method == "OPTIONS":
            return await call_next(request)

        # IP Whitelist and Secret Key Config
        WHITELISTED_IPS = settings.ADMIN_WHITELISTED_IPS  # List of IPs allowed
        SUPERUSER_SECRET_KEY = settings.SUPERUSER_CREATION_SECRET_KEY

        # Define routes requiring special handling
        CREATE_ROUTE = "/api/admin/create"
        LOGIN_ROUTE = "/api/admin/login"

        # Handle the `/create` route (requires white-listed IP and secret key)
        if request.url.path == CREATE_ROUTE:
            client_ip = request.client.host
            provided_secret_key = request.headers.get("X-Superuser-Secret")
            if not provided_secret_key:
                logger.warning("No superuser secret key provided in the headers.")
                return JSONResponse(
                    {"detail": "Missing superuser secret key."},
                    status_code=403,
                )

            # Validate IP
            if client_ip not in WHITELISTED_IPS:
                logger.warning(f"Unauthorized IP for /create: {client_ip}")
                return JSONResponse(
                    {"detail": "Access denied. Unauthorized IP."},
                    status_code=403,
                )

            # Validate secret key
            if provided_secret_key != SUPERUSER_SECRET_KEY:
                logger.warning("Invalid superuser secret key for /create.")
                return JSONResponse(
                    {"detail": "Invalid secret key."},
                    status_code=403,
                )

            # If valid, allow the request
            return await call_next(request)

        # Handle the `/login` route (exempted from IP and token validation)
        if request.url.path == LOGIN_ROUTE:
            return await call_next(request)

        # For other `/api/admin` routes, perform session validation
        if request.url.path.startswith("/api/admin"):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                logger.warning("Missing or invalid Authorization header.")
                return JSONResponse(
                    {"detail": "Unauthorized: Missing or invalid token"},
                    status_code=401,
                )

            token = auth_header.split(" ")[1]

            try:
                # Validate the session
                db = next(get_db())
                validate_session(token, db)
            except Exception as e:
                logger.error(f"Session validation failed for {request.url.path}: {e}")
                return JSONResponse(
                    {"detail": "Unauthorized: Invalid session"},
                    status_code=401,
                )

        # For all other routes, allow the request to proceed
        return await call_next(request)
