from pydantic import BaseModel


class RecommendMusicRequest(BaseModel):
    genres: list[str]
