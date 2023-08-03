from pydantic import BaseModel
from .artist import Artist
from datetime import date


class Song(BaseModel):
    id: str
    genie_id: str
    title: str
    artist: Artist
    released_date: date
    like_cnt: int
    spotify_url: str | None
