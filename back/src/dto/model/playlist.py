from pydantic import BaseModel
from .song import Song


class Playlist(BaseModel):
    id: str
    genie_id: str
    title: str
    like_cnt: int
    view_cnt: int
    tags: list[str]
    songs: list[Song]
    img_url: str
