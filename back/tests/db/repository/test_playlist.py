import unittest
from datetime import date
from src import db
from .common import connect_to_db
from src.db.repository import (
    PlaylistRepository,
    SongRepository,
    ArtistRepository,
)
from src.db.exception import (
    NotFoundPlaylistException,
    NotFoundSongException,
)
from src.dto.model import Playlist, Song, Artist


class TestPlaylist(unittest.TestCase):
    songRepository = SongRepository()
    playlistRepository = PlaylistRepository()
    artistRepository = ArtistRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_playlist(self):
        artist = self.__artist()
        song = self.__song(artist=artist, genie_id="S1")
        self.__playlist(songs=[song], genie_id="1")

        # not exists song
        fake_song = Song(id="1234", genie_id="S3", title="title", artist=artist, released_date=date.today(), like_cnt=10, spotify_url=None)
        self.assertRaises(NotFoundSongException, lambda: self.__playlist(songs=[fake_song], genie_id="2"))

    def test_delete_by_genie_id(self):
        artist = self.__artist()
        song = self.__song(artist=artist)
        playlist = self.__playlist(songs=[song])

        self.playlistRepository.delete_by_genie_id(playlist.genie_id)
        found = self.playlistRepository.find_by_genie_id(playlist.genie_id)
        assert found is None

        # not exists playlist
        self.assertRaises(
            NotFoundPlaylistException,
            lambda: self.playlistRepository.delete_by_genie_id(playlist.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = self.__artist()
        song = self.__song(artist=artist)
        playlist = self.__playlist(songs=[song])

        found = self.playlistRepository.find_by_genie_id(playlist.genie_id)
        assert playlist == found

    def test_find_all(self):
        artist = self.__artist()
        song = self.__song(artist=artist)

        playlists = [
            self.__playlist(songs=[song], genie_id="P1"),
            self.__playlist(songs=[song], genie_id="P2"),
            self.__playlist(songs=[song], genie_id="P3"),
        ]

        found = self.playlistRepository.find_all()
        for playlist in playlists:
            assert playlist in found

    def __song(
        self,
        artist: Artist,
        genie_id: str = "S1",
        title: str = "노래",
        released_date: date = date.today(),
        like_cnt: int = 10,
        spotify_url: str = "http://song.mp4",
    ) -> Song:
        return self.songRepository.create_song(genie_id, title, artist, released_date, like_cnt, spotify_url)

    def __artist(self, genie_id: str = "A1", name: str = "주혜인") -> Artist:
        return self.artistRepository.create_artist(genie_id, name)

    def __playlist(
        self,
        songs: list[Song],
        genie_id: str = "P1",
        title: str = "주혜인의 플리",
        like_cnt: int = 10,
        view_cnt: int = 20,
        tags: list[str] = ["tag"],
        img_url: str = "http://pl.png",
    ) -> Playlist:
        return self.playlistRepository.create_playlist(genie_id, title, like_cnt, view_cnt, tags, songs, img_url)
