from fastapi import APIRouter, UploadFile, File, Depends
from uuid import uuid4

from src.router.dto.RecommendMusicRequest import RecommendMusicRequest
from src.router.dto.RecommendMusicResponse import RecommendMusicResponse, RecommendMusic
from src.infer.playlist import PlaylistIdExtractor
from src.log.Logger import get_user_logger
from . import SaveFile
router = APIRouter()

user_logger = get_user_logger()

pl_k = 3
song_k = 6  # song_k must be more than 6 or loop of silder must be False

playlist = PlaylistIdExtractor(k=pl_k, is_data_pull=False)

@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...), data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form)
) -> RecommendMusicResponse:

    session_id = str(uuid4()).replace("-","_")
    user_logger.info("Session ID : %s", session_id)
    SaveFile.save_file(session_id, image, user_logger)
    user_logger.info("Genres : %s", data)

    pl_ids = []
    pl_ids.extend(playlist.get_weather_playlist_id(image))
    # pl_ids.extend(playlist.get_mood_playlist_id(image))  # place for mood playlist id
    # pl_ids.extend(playlist.get_sit_playlist_id(image))  # place for situation playlist id
    user_logger.info("Playlist IDs : %s", pl_ids)

    # song_ids = get_songs_from_pls(pl_ids)
    # top_songs = get_top_songs_with_step_3(song_ids, side_info_like_genres)
    # logger.info("Song IDs : %s", top_songs)

    songs = [
        RecommendMusic(song_id=1, youtube_id="XHMdIA6bEOE", song_title="짱구는 못말려 오프닝1", artist_name="아이브", album_title="짱구 1기"),
        RecommendMusic(
            song_id=2,
            youtube_id="Sq_mS6xWpvk",
            song_title="Kiss Goodnightrrrrrrrrrr",
            artist_name="I Dont Know How But They Found Meeeee",
            album_title="Razzmatazz",
        ),
        RecommendMusic(
            song_id=3,
            youtube_id="A1tZgPAcpjE",
            song_title="사랑하긴 했었나요 스쳐가는 인연이었나요 짧지않은 우리 함께했던 시간들이 자꾸 내 마음을 가둬두네",
            artist_name="잔나비 잔나비 잔미잔미 잔나비 잔나비 잔미잔미",
            album_title="봉춤을 추네",
        ),
        RecommendMusic(song_id=4, youtube_id="NbKH4iZqq1Y", song_title="Drowning", artist_name="WOODZ", album_title="OO-LI"),
        RecommendMusic(song_id=5, youtube_id="2Kff0U8w-aU", song_title="OMG", artist_name="NewJeans", album_title="NewJeans 'OMG'"),
        RecommendMusic(song_id=6, youtube_id="j1uXcHwLhHM", song_title="사건의 지평선", artist_name="윤하", album_title="END THEORY : Final Edition"),
    ]
    user_logger.info("Recommend Songs : %s",  songs)

    return RecommendMusicResponse(session_id=session_id,songs=songs)

