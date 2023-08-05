import unittest
from datetime import date
from src import db
from .common import connect_to_db
from src.db.repository import (
    SongRepository,
    ArtistRepository,
)
from src.db.exception import (
    NotFoundSongException,
    NotFoundArtistException,
)
from src.dto.model import Artist, Song


class TestSong(unittest.TestCase):
    songRepository = SongRepository()
    artistRepository = ArtistRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_song(self):
        artist = self.__artist()
        self.__song(artist=artist, genie_id="S1")

        # not exists artist
        fake_artist = Artist(id="123", genie_id="A3", name="없는것")
        self.assertRaises(NotFoundArtistException, lambda: self.__song(artist=fake_artist, genie_id="S2"))

    def test_delete_by_genie_id(self):
        artist = self.__artist()
        song = self.__song(artist=artist)

        self.songRepository.delete_by_genie_id(song.genie_id)
        found = self.songRepository.find_by_genie_id(song.genie_id)
        assert found is None

        # not exists song
        self.assertRaises(
            NotFoundSongException,
            lambda: self.songRepository.delete_by_genie_id(song.genie_id),
        )

    def test_find_by_geine_id(self):
        artist = self.__artist()
        song = self.__song(artist=artist)

        found = self.songRepository.find_by_genie_id(song.genie_id)
        assert song == found

    def test_find_all(self):
        artist = self.__artist()
        songs = [
            self.__song(artist=artist, genie_id="S1"),
            self.__song(artist=artist, genie_id="S2"),
            self.__song(artist=artist, genie_id="S3"),
        ]

        found = self.songRepository.find_all()
        for song in songs:
            assert song in found

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
