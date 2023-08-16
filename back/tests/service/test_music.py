import unittest
from unittest.mock import Mock, patch
from datetime import datetime, date
from logging import Logger
from src.services.music import MusicService
from src.config import AppConfig
from src.db import PlaylistRepository, Song, Album, Artist
from src.infer.playlist import PlaylistIdExtractor
from src.infer.song import SongExtractor
from src.dto.request import RecommendMusicRequest


class TestMusicService(unittest.TestCase):
    def setUp(self) -> None:
        self.app_config = AppConfig()
        self.user_logger: Logger = Mock()
        self.playlist_repository: PlaylistRepository = Mock()
        self.playlist_id_ext: PlaylistIdExtractor = Mock()
        self.song_ext: SongExtractor = Mock()

        self.music_service = MusicService(self.user_logger, self.playlist_repository, self.playlist_id_ext, self.song_ext)

    def mock_api_functions_of_playlist_id_ext(self):
        self.playlist_id_ext.get_weather_playlist_id.return_value = ([0.1] * 15, list(range(1, 16)))
        self.playlist_id_ext.get_mood_playlist_id.return_value = ([0.1] * 15, list(range(3, 18)))
        self.playlist_id_ext.get_sit_playlist_id.return_value = ([0.1] * 15, list(range(5, 20)))

    def mock_api_functions_of_song_ext(self):
        songs = []
        for i in range(45):
            album = Album(
                id=str(i),
                genie_id=str(i),
                name=f"name_{i}",
                img_url=f"url_{i}",
                released_date=date.today(),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            artist = Artist(
                id=str(i),
                genie_id=str(i),
                name=f"name_{i}",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            song = Song(
                id=str(i),
                genie_id=str(i),
                title=f"title_{i}",
                lyrics=f"lyrics_{i}",
                album=album,
                artist=artist,
                like_cnt=i,
                listener_cnt=i,
                play_cnt=i,
                genres=["POP", "락"],
                spotify_url=f"spotify_url_{i}",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            songs.append(song)
        self.song_ext.extract_songs.return_value = songs

    @patch("src.services.music.save_file", autospec=True)
    @patch("src.services.music.resize_img")
    def test_recommend_music(self, resize_img, save_file):
        self.mock_api_functions_of_playlist_id_ext()
        self.mock_api_functions_of_song_ext()

        image = Mock()
        data = RecommendMusicRequest(genres=["POP", "락"])

        response = self.music_service.recommend_music(image, data)

        self.assertIsNotNone(response.session_id)
        self.assertIsNotNone(response.songs)
