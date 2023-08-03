from pydantic import BaseModel
from fastapi import Form


class RecommendMusicRequest(BaseModel):
    genres: list[str]

    @classmethod
    def as_form(cls, genres: list[str] = Form()):
        genres_ = genres[0].split(",")
        return cls(genres=genres_)
