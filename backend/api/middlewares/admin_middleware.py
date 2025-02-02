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
        if request.method == "OPTIONS":
            return await call_next(request)

        WHITELISTED_IPS = settings.ADMIN_WHITELISTED_IPS
        SUPERUSER_SECRET_KEY = settings.SUPERUSER_CREATION_SECRET_KEY

        EXEMPT_ROUTES = [
            "/api/admin/create",
            "/api/admin/login",
            "/api/admin/mfa/setup",
            "/api/admin/mfa/verify",
        ]

        logger.debug(f"Processing admin request to: {request.url.path}")

        if request.url.path in EXEMPT_ROUTES:
            if request.url.path == "/api/admin/create":
                client_ip = request.client.host
                provided_secret_key = request.headers.get("X-Superuser-Secret")

                if not provided_secret_key:
                    logger.warning("Missing superuser secret key.")
                    return JSONResponse({"detail": "Missing superuser secret key."}, status_code=403)

                if client_ip not in WHITELISTED_IPS:
                    logger.warning(f"Unauthorized IP: {client_ip}")
                    return JSONResponse({"detail": "Access denied. Unauthorized IP."}, status_code=403)

                if provided_secret_key != SUPERUSER_SECRET_KEY:
                    logger.warning("Invalid superuser secret key.")
                    return JSONResponse({"detail": "Invalid secret key."}, status_code=403)

            return await call_next(request)

        if request.url.path.startswith("/api/admin"):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                logger.warning("Missing or invalid Authorization header.")
                return JSONResponse({"detail": "Unauthorized: Missing or invalid token"}, status_code=401)

            token = auth_header.split(" ")[1]

            try:
                db = next(get_db())
                validate_session(token, db)
            except Exception as e:
                logger.error(f"Session validation failed: {e}")
                return JSONResponse({"detail": "Unauthorized: Invalid session"}, status_code=401)

        return await call_next(request)
