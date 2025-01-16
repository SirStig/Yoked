from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import api_router
from backend.api.health import health_router
from core.database import engine, Base

# Create all database tables on application startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fitness Foundry API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],  # Adjust as needed
    allow_headers=["*"],  # Adjust as needed
)


@app.on_event("startup")
async def startup():
    """
    Database connection on startup.
    """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """
    Database connection close on shutdown.
    """
    await database.disconnect()


# Include API routers
app.include_router(api_router)
app.include_router(health_router, prefix="/health")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)