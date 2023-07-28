from pydantic import BaseModel
from fastapi import Form


class RecommendMusic(BaseModel):
    song_id: int
    song_title: str
    artist_name: str
    album_title: str
    music_url: str


class RecommendMusicResponse(BaseModel):
    session_id: str
    songs: list[RecommendMusic]


class RecommendMusicRequest(BaseModel):
    genres: list[str]

    @classmethod
    def as_form(cls, genres: list[str] = Form()):
        genres_ = genres[0].split(",")
        return cls(genres=genres_)
