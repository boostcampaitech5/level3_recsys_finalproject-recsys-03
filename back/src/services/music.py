import pandas as pd
from fastapi import UploadFile
from uuid import uuid4
from src.infer.playlist import PlaylistIdExtractor
from src.infer.song import SongIdExtractor
from src.infer.spotify import get_spotify_url
from src.log.logger import get_user_logger
from src.dto.music import RecommendMusicRequest, RecommendMusicResponse, RecommendMusic
from src.services.utils import save_file, resize_img

pl_k = 15
top_k = 6  # song_k must be more than 6 or loop of silder must be False
SIZE = 224


class MusicService:
    def __init__(self) -> None:
        self.user_logger = get_user_logger()

        self.playlist_id_ext = PlaylistIdExtractor(k=pl_k, is_data_pull=True)
        self.song_id_ext = SongIdExtractor(is_data_pull=True)

    def recommend_music(self, image: UploadFile, data: RecommendMusicRequest) -> list[RecommendMusic]:
        session_id = str(uuid4()).replace("-", "_")
        img_path = save_file(session_id, image)
        resize_img(img_path, SIZE)

        pl_ids, pl_scores = self._extract_playlist_ids(img_path)
        song_df = self._extract_songs(data.genres, pl_ids, pl_scores, top_k)

        songs = [
            RecommendMusic(
                song_id=int(song_df.iloc[i]["song_id"]),
                song_title=song_df.iloc[i]["song_title"],
                artist_name=song_df.iloc[i]["artist_name"],
                album_title=song_df.iloc[i]["album_title"],
                music_url=song_df.iloc[i]["music_url"],
            )
            for i in range(song_df.shape[0])
        ]

        self.user_logger.info(
            {
                "session_id": session_id,
                "Img Path": img_path,
                "Genres": data.genres,
                "Playlist IDs": pl_ids,
                "Recommend Songs": songs,
            }
        )

        return RecommendMusicResponse(session_id=session_id, songs=songs)

    def _extract_playlist_ids(self, img_path: str) -> tuple[list[int], list[float]]:
        pl_scores, pl_ids = [], []

        weather_scores, weather_ids = self.playlist_id_ext.get_weather_playlist_id(img_path)
        sit_scores, sit_ids = self.playlist_id_ext.get_mood_playlist_id(img_path)
        mood_scores, mood_ids = self.playlist_id_ext.get_sit_playlist_id(img_path)

        pl_scores.extend(weather_scores)
        pl_scores.extend(sit_scores)
        pl_scores.extend(mood_scores)
        pl_ids.extend(weather_ids)
        pl_ids.extend(sit_ids)
        pl_ids.extend(mood_ids)

        return pl_ids, pl_scores

    def _extract_songs(self, genres: list[str], pl_ids: list[int], pl_scores: list[float], top_k: int) -> pd.DataFrame:
        song_infos = self.song_id_ext.get_song_info(pl_ids, pl_scores, genres)
        return get_spotify_url(song_infos, top_k)
