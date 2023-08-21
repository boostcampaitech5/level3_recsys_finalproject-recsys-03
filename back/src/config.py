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

    # model
    hub_path: str = "./hub"
    model_repo: str = "Recdol/PL_Multilabel"

    weather_model_version: str = "weather-25_150958"
    sit_model_version: str = "sit-25_133334"
    mood_model_version: str = "mood-25_144428"

    weather_index_version: str = "weather-25_150958"
    sit_index_version: str = "sit-25_133334"
    mood_index_version: str = "mood-25_144428"

    class Config:
        env_file = ".env"
