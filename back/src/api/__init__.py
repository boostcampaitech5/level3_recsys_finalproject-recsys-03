from fastapi import APIRouter

from src.api import feedback, music

router = APIRouter()
router.include_router(music.router, tags=["music"])
router.include_router(feedback.router, tags=["feedback"])


__all__ = ["router"]
