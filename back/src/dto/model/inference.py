from pydantic import BaseModel
from .user import User
from .song import Song
from .playlist import Playlist


class SongsElement(BaseModel):
    song: Song
    is_like: bool


class Inference(BaseModel):
    id: str
    user: User
    query_img_url: str
    playlists: list[Playlist]
    songs: list[SongsElement]
    genres: list[str]
