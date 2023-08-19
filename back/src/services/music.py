from fastapi import UploadFile
from uuid import uuid4
from ..infer.playlist import PlaylistIdExtractor
from ..infer.song import SongExtractor
from ..dto.response import RecommendMusicResponse, RecommendMusic
from ..dto.request import RecommendMusicRequest
from ..db import Playlist, Song, PlaylistRepository, NotFoundPlaylistException
from .utils import save_file, resize_img
from logging import Logger


top_k = 6  # song_k must be more than 6 or loop of silder must be False
SIZE = 224


class MusicService:
    def __init__(
        self, logger: Logger, playlist_repository: PlaylistRepository, playlist_id_ext: PlaylistIdExtractor, song_ext: SongExtractor
    ) -> None:
        self.user_logger = logger
        self.playlist_repository = playlist_repository
        self.playlist_id_ext = playlist_id_ext
        self.song_ext = song_ext

    def recommend_music(self, image: UploadFile, data: RecommendMusicRequest) -> RecommendMusicResponse:
        session_id = str(uuid4()).replace("-", "_")
        img_path = save_file(session_id, image)
        resize_img(img_path, SIZE)

        playlists, pl_scores = self._extract_playlists(img_path)
        pl_genie_ids = [playlist.genie_id for playlist in playlists]
        songs = self._extract_songs(data.genres, playlists, pl_scores, top_k)

        songs = [
            RecommendMusic(
                song_id=int(song.genie_id),
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

        playlists = [self._find_pl_by_genie_id(str(pl_id)) for pl_id in pl_ids]
        return playlists, pl_scores

    def _extract_songs(self, genres: list[str], playlists: list[Playlist], pl_scores: list[float], top_k: int) -> list[Song]:
        songs = self.song_ext.extract_songs(playlists, pl_scores, genres)
        return songs[:top_k]

    def _find_pl_by_genie_id(self, genie_id: str):
        found = self.playlist_repository.find_by_genie_id(genie_id)
        if found is None:
            raise NotFoundPlaylistException(f"DB에서 genie_id={genie_id}인 playlist를 찾을 수 없습니다!")
        return found
