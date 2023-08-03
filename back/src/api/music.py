from fastapi import APIRouter, UploadFile, File, Depends
from ..dto.response import RecommendMusicResponse
from ..dto.request import RecommendMusicRequest
from ..services.music import MusicService


music_service = MusicService()
router = APIRouter()


@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...), data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form)
) -> RecommendMusicResponse:
    return music_service.recommend_music(image, data)
