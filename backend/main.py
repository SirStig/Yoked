import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.api.auth.auth_routes import router as auth_router
from backend.api.users.user_routes import router as user_router
from backend.api.workouts.workout_routes import router as workout_router
import logging

from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from backend.core.database import init_db

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for Fitness Foundry",
    debug=settings.DEBUG
)

# HTTPS Middleware
if not settings.DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="static")

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    logger.info("Starting the application...")
    init_db()
    logger.info("Database initialized.")

# Register routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(workout_router, prefix="/api/workouts", tags=["Workouts"])

# Health Check Endpoint
@app.get("/health", tags=["System"])
def health_check():
    logger.debug("Health check accessed.")
    return {"status": "ok", "environment": settings.ENV}

# Run server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        ssl_keyfile=settings.SSL_KEYFILE if not settings.DEBUG else None,
        ssl_certfile=settings.SSL_CERTFILE if not settings.DEBUG else None
    )
