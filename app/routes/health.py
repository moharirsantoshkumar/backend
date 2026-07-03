from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health():
    return {
        "status": "UP",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/ready")
def readiness():
    return {
        "ready": True
    }


@router.get("/live")
def liveness():
    return {
        "alive": True
    }