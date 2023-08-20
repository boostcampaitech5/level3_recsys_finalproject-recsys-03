from fastapi import APIRouter, UploadFile, File, Depends
from ..dto.response import RecommendMusicResponse
from ..dto.request import RecommendMusicRequest
from ..services.music import MusicService
from ..infer.playlist import PlaylistIdExtractor
from ..infer.song import SongExtractor
from ..db import PlaylistRepository
from ..log.logger import get_user_logger
from ..config import AppConfig

config = AppConfig()

pl_k = 15

user_logger = get_user_logger()
playlist_repository = PlaylistRepository()
playlist_id_ext = PlaylistIdExtractor(config=config, k=pl_k, is_data_pull=True)
song_ext = SongExtractor()

music_service = MusicService(user_logger, playlist_repository, playlist_id_ext, song_ext)
router = APIRouter()


@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...), data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form)
) -> RecommendMusicResponse:
    return music_service.recommend_music(image, data)
