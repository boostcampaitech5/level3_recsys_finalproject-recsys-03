from pydantic import BaseModel
from .artist import Artist
from datetime import datetime


class Song(BaseModel):
    id: str
    genie_id: int
    title: str
    artist: Artist
    released_date: datetime
    like_cnt: int
    spotify_url: str | None
