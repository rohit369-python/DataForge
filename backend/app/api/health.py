"""Health and service-status endpoints."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """Return a lightweight liveness response."""
    return {"status": "healthy", "service": "datapulse-api"}
