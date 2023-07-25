from fastapi import APIRouter, UploadFile, File, Depends
from uuid import uuid4

from src.router.dto.recommend_music_request import RecommendMusicRequest
from src.router.dto.recommend_music_response import RecommendMusicResponse, RecommendMusic
from src.router.dto.user_feedback_request import UserFeedbackRequest
from src.infer.playlist import PlaylistIdExtractor
from src.infer.song import SongIdExtractor
from src.log.logger import get_user_logger, get_feedback_logger
from src.router.preprocess import save_file, resize_img
from src.infer.spotify import get_spotify_url


router = APIRouter()

user_logger = get_user_logger()
feedback_logger = get_feedback_logger()

pl_k = 3
song_k = 15
top_k = 6  # song_k must be more than 6 or loop of silder must be False
SIZE = 224

playlist = PlaylistIdExtractor(k=pl_k, is_data_pull=True)
song = SongIdExtractor(k=song_k, is_data_pull=True)


@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...), data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form)
) -> RecommendMusicResponse:
    session_id = str(uuid4()).replace("-", "_")
    img_path = save_file(session_id, image)
    resize_img(img_path, SIZE)

    pl_scores, pl_ids = [], []

    weather_scores, weather_ids = playlist.get_weather_playlist_id(img_path)
    sit_scores, sit_ids = playlist.get_mood_playlist_id(img_path)
    mood_scores, mood_ids = playlist.get_sit_playlist_id(img_path)

    pl_scores.extend(weather_scores)
    pl_scores.extend(sit_scores)
    pl_scores.extend(mood_scores)
    pl_ids.extend(weather_ids)
    pl_ids.extend(sit_ids)
    pl_ids.extend(mood_ids)

    user_genres = [genre for genre in data.genres[0].split(",")]
    infos = song.get_song_info(pl_ids, pl_scores, user_genres, song_k)
    songs = get_spotify_url(infos, top_k)

    songs = [
        RecommendMusic(
            song_id=int(songs.iloc[i]["song_id"]),
            youtube_id=songs.iloc[i]["youtube_key"],
            song_title=songs.iloc[i]["song_title"],
            artist_name=songs.iloc[i]["artist_name"],
            album_title=songs.iloc[i]["album_title"],
            music_url=songs.iloc[i]["music_url"],
        )
        for i in range(songs.shape[0])
    ]

    user_logger.info(
        {
            "session_id": session_id,
            "Img Path": img_path,
            "Genres": [genre for genre in data.genres[0].split(",")],
            "Playlist IDs": pl_ids,
            "Recommend Songs": songs,
        }
    )

    return RecommendMusicResponse(session_id=session_id, songs=songs)


@router.post("/userFeedback")
async def user_feedback(data: UserFeedbackRequest) -> None:
    feedback_logger.info(
        {
            "session Id": data.session_id,
            "song Id": data.song_id,
            "thumbs up": data.thumbs_up,
            "thumbs down": data.thumbs_down,
        }
    )
