from fastapi import UploadFile
from uuid import uuid4
from ..infer.playlist import PlaylistIdExtractor
from ..infer.song import SongIdExtractor
from ..log.logger import get_user_logger
from ..dto.response import RecommendMusicResponse, RecommendMusic
from ..dto.request import RecommendMusicRequest
from ..db import Playlist, Song, PlaylistRepository, SongRepository
from .utils import save_file, resize_img

pl_k = 15
top_k = 6  # song_k must be more than 6 or loop of silder must be False
SIZE = 224


class MusicService:
    def __init__(self) -> None:
        self.user_logger = get_user_logger()

        self.playlist_id_ext = PlaylistIdExtractor(k=pl_k, is_data_pull=True)
        self.song_id_ext = SongIdExtractor(is_data_pull=True)

        self.song_repository = SongRepository()
        self.playlist_repository = PlaylistRepository()

    def recommend_music(self, image: UploadFile, data: RecommendMusicRequest) -> RecommendMusicResponse:
        session_id = str(uuid4()).replace("-", "_")
        img_path = save_file(session_id, image)
        resize_img(img_path, SIZE)

        playlists, pl_scores = self._extract_playlists(img_path)
        pl_genie_ids = [playlist.genie_id for playlist in playlists]
        songs = self._extract_songs(data.genres, playlists, pl_scores, top_k)

        songs = [
            RecommendMusic(
                song_id=song.id,
                song_title=song.title,
                artist_name=song.artist.name,
                album_title=song.album.name,
                music_url=song.spotify_url,
            )
            for song in songs
        ]

        self.user_logger.info(
            {
                "session_id": session_id,
                "Img Path": img_path,
                "Genres": data.genres,
                "Playlist IDs": pl_genie_ids,
                "Recommend Songs": songs,
            }
        )

        return RecommendMusicResponse(session_id=session_id, songs=songs)

    def _extract_playlists(self, img_path: str) -> tuple[list[Playlist], list[float]]:
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

        playlists = [self.playlist_repository.find_by_genie_id(pl_id) for pl_id in pl_ids]
        return playlists, pl_scores

    def _extract_songs(self, genres: list[str], playlists: list[Playlist], pl_scores: list[float], top_k: int) -> list[Song]:
        pl_ids = [playlist.genie_id for playlist in playlists]
        song_infos = self.song_id_ext.get_song_info(pl_ids, pl_scores, genres)

        song_ids = (song_info["song_id"] for song_info in song_infos)
        return [self.song_repository.find_by_genie_id(song_id) for song_id in song_ids]
