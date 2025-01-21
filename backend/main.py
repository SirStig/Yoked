import subprocess
import signal
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.api.payments.webhooks.stripe_webhook import stripe_webhook
from backend.core.config import settings
from backend.api.auth.auth_routes import router as auth_router
from backend.api.users.user_routes import router as user_router
from backend.api.payments.payment_routes import router as payment_router
from backend.api.workouts.workout_routes import router as workout_router
from backend.api.payments.webhooks.stripe_webhook import router as stripe_webhook
from backend.api.subscriptions.subscription_routes import router as subscription_router
from backend.api.middlewares.session_middleware import SessionValidationMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from backend.core.database import init_db, get_db
from backend.core.logging_config import get_logger

# Initialize logging
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=f"{settings.APP_NAME} API",
    version=settings.APP_VERSION,
    description="Welcome to the Yoked Fitness API",
    debug=settings.DEBUG,
)

# Middleware: HTTPS
if not settings.DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)
    logger.info("HTTPS redirect middleware added (Production mode).")

# Parse ALLOWED_HOSTS from settings
allowed_origins = settings.ALLOWED_HOSTS.split(",")

@app.middleware("http")
async def log_request(request: Request, call_next):
    logger.info(f"Processing request {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Middleware: Inject DB Session
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = get_db
    response = await call_next(request)
    return response

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS middleware configured with origins: {allowed_origins}")

# Celery processes
celery_worker = None
celery_beat = None

def start_celery():
    """
    Start Celery worker and beat scheduler.
    """
    global celery_worker, celery_beat
    try:
        # Start Celery worker
        celery_worker = subprocess.Popen(
            ["celery", "-A", "backend.tasks.celery_app", "worker", "--loglevel=info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info("Celery worker started.")

        # Start Celery beat scheduler
        celery_beat = subprocess.Popen(
            ["celery", "-A", "backend.tasks.celery_app", "beat", "--loglevel=info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.info("Celery beat scheduler started.")
    except Exception as e:
        logger.error(f"Failed to start Celery: {e}")
        raise

def stop_celery():
    """
    Stop Celery worker and beat scheduler.
    """
    global celery_worker, celery_beat
    try:
        if celery_worker:
            celery_worker.terminate()
            celery_worker.wait()
            logger.info("Celery worker stopped.")

        if celery_beat:
            celery_beat.terminate()
            celery_beat.wait()
            logger.info("Celery beat scheduler stopped.")
    except Exception as e:
        logger.error(f"Error stopping Celery: {e}")

# Middleware: Session Validation
try:
    app.add_middleware(SessionValidationMiddleware)
    logger.info("Session validation middleware added.")
except Exception as e:
    logger.error(f"Failed to add session middleware: {e}")

# Static files for frontend
try:
    app.mount("/static", StaticFiles(directory="../frontend/build", html=True), name="static")
    logger.info("Static files mounted for frontend.")
except Exception as e:
    logger.error(f"Failed to mount static files: {e}")

# Register Routers
try:
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    logger.info("Auth router registered.")
except Exception as e:
    logger.error(f"Failed to register auth router: {e}")

try:
    app.include_router(user_router, prefix="/api/users", tags=["Users"])
    logger.info("User router registered.")
except Exception as e:
    logger.error(f"Failed to register user router: {e}")

try:
    app.include_router(workout_router, prefix="/api/workouts", tags=["Workouts"])
    logger.info("Workout router registered.")
except Exception as e:
    logger.error(f"Failed to register workout router: {e}")

try:
    app.include_router(payment_router, prefix="/api/payments", tags=["Payments"])
    logger.info("Payment router registered.")
except Exception as e:
    logger.error(f"Failed to register Payment router: {e}")

try:
    app.include_router(subscription_router, prefix="/api/subscriptions", tags=["Subscriptions"])
    logger.info("Subscription router registered.")
except Exception as e:
    logger.error(f"Failed to register Subscription router: {e}")

try:
    app.include_router(stripe_webhook, prefix="/stripe/webhooks", tags=["StripeWebhooks"])
    logger.info("Stripe Webhook router registered.")
except Exception as e:
    logger.error(f"Failed to register Stripe Webhook router: {e}")

# Startup Event
@app.on_event("startup")
def on_startup():
    logger.info("Starting application initialization...")
    try:
        init_db()
        logger.info("Database initialized.")
        start_celery()
    except Exception as e:
        logger.critical(f"Startup failure: {e}")
        raise RuntimeError("Application startup failed.")

# Shutdown Event
@app.on_event("shutdown")
def on_shutdown():
    logger.info("Shutting down application...")
    stop_celery()

# Health Check
@app.get("/health", tags=["System"])
def health_check():
    logger.debug("Health check endpoint accessed.")
    return {"status": "ok", "environment": settings.ENV}

# Run server
if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    try:
        uvicorn.run(
            "backend.main:app",
            host=settings.HOST,
            port=8000,
            reload=settings.DEBUG,
            ssl_keyfile=settings.SSL_KEYFILE if not settings.DEBUG else None,
            ssl_certfile=settings.SSL_CERTFILE if not settings.DEBUG else None,
        )
    except Exception as e:
        logger.critical(f"Failed to start Uvicorn server: {e}")
