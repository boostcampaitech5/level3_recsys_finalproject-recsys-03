from pydantic import BaseModel


class RecommendMusic(BaseModel):
    song_id: int
    song_title: str
    artist_name: str
    album_title: str
    youtube_id: str


class RecommendMusicResponse(BaseModel):
    songs: list[RecommendMusic]
