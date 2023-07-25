from pydantic import BaseModel


class UserFeedbackRequest(BaseModel):
    session_id: str
    song_id: int
    is_like: bool
