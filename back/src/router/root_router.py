from fastapi import APIRouter, UploadFile, File, Depends
from uuid import uuid4

from src.router.dto.RecommendMusicRequest import RecommendMusicRequest
from src.router.dto.RecommendMusicResponse import RecommendMusicResponse, RecommendMusic
from src.infer.playlist import PlaylistIdExtractor
from src.infer.song import SongIdExtractor
from src.log.Logger import get_user_logger
from src.router.SaveFile import save_file


router = APIRouter()

user_logger = get_user_logger()

pl_k = 3
song_k = 6  # song_k must be more than 6 or loop of silder must be False


playlist = PlaylistIdExtractor(k=pl_k, is_data_pull=False)
song = SongIdExtractor(k=song_k, is_data_pull=False)



@router.post("/recommendMusic")
async def recommend_music(
    image: UploadFile = File(...), data: RecommendMusicRequest = Depends(RecommendMusicRequest.as_form)
) -> RecommendMusicResponse:
    session_id = str(uuid4()).replace("-", "_")
    img_path = save_file(session_id, image)

    pl_scores, pl_ids = [], []
    w_scores, w_ids = playlist.get_weather_playlist_id(img_path)
    pl_scores.extend(w_scores)
    pl_ids.extend(w_ids)
    
    #pl_ids.extend(playlist.get_mood_playlist_id(img_path))  # place for mood playlist id
    #pl_ids.extend(playlist.get_sit_playlist_id(img_path))  # place for situation playlist id
    
    user_genres = [genre for genre in data.genres[0].split(",")]
    songs = song.get_song_info(pl_ids, pl_scores, user_genres)
    
    songs=[RecommendMusic(
        song_id=int(songs.iloc[i]["song_id"]),
        youtube_id=songs.iloc[i]["youtube_key"],
        song_title=songs.iloc[i]["song_title"],
        artist_name=songs.iloc[i]["artist_name"],
        album_title=songs.iloc[i]["album_title"],) for i in range(songs.shape[0])]

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
