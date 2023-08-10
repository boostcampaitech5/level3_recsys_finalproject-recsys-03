from pydantic import BaseModel


class ReLoginRequest(BaseModel):
    refresh_token: str
