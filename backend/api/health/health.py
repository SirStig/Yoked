from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "healthy"}