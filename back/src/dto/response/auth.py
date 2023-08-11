from pydantic import BaseModel


class SigninResponse(BaseModel):
    access_token: str
    refresh_token: str


class ReLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
