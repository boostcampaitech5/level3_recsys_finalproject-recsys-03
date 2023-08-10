from fastapi import APIRouter

from src.api import feedback, music, auth

router = APIRouter()
router.include_router(music.router, tags=["music"])
router.include_router(feedback.router, tags=["feedback"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])


__all__ = ["router"]
