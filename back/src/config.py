from pydantic_settings import BaseSettings
from datetime import timedelta


class AppConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    spotify_cid: str
    spotify_pwd: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str

    # json web token
    jwt_secret: str
    access_token_exp_period: timedelta = timedelta(hours=1)
    refresh_token_exp_period: timedelta = timedelta(days=1)

    class Config:
        env_file = ".env"
