from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    spotify_cid: str
    spotify_pwd: str
    db_host: str
    db_name: str
    db_username: str
    db_password: str

    class Config:
        env_file = ".env"
