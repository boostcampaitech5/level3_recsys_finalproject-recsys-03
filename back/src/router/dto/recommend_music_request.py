from pydantic import BaseModel
from fastapi import Form


class RecommendMusicRequest(BaseModel):
    genres: list[str]

    @classmethod
    def as_form(cls, genres: list[str] = Form(...)):
        return cls(genres=genres)
