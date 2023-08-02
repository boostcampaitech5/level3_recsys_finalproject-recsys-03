from pydantic import BaseModel


class Artist(BaseModel):
    id: str
    genie_id: str
    name: str
