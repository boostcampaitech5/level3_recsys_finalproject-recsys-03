from pydantic import BaseModel
from .user import User
from datetime import datetime


class Auth(BaseModel):
    id: str
    user: User
    refresh_token: str
    created_at: datetime
