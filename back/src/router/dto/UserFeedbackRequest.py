from pydantic import BaseModel


class UserFeedbackRequest(BaseModel):
    session_id: str
    song_id: int
    thumbs_up: bool
    thumbs_down: bool
