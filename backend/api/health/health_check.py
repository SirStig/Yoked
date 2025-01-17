from fastapi import APIRouter
from backend.core.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    logger.info("Health check endpoint hit")
    return {"status": "ok", "message": "Backend is running"}

