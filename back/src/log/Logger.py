import logging
import logging.config
from src.utils import create_dir
from pythonjsonlogger import jsonlogger


OUTPUT_PATH = "outputs/logs"
USER_LOG_PATH = OUTPUT_PATH + "/user_log.log"
API_LOG_PATH = OUTPUT_PATH + "/api_log.log"

logger_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "basic": {"format": "%(asctime)s | %(levelname)s - %(message)s"},
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(filename)s %(session_id)s %(Img Path)s %(Genres)s %(Playlist IDs)s %(Recommend Songs)s",
        },
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "basic"},
        "user_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter": "json",
            "encoding": "utf-8",
            "filename": USER_LOG_PATH,
            "maxBytes": 1e7,
            "backupCount": 100,
        },
        "api_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter": "basic",
            "encoding": "utf-8",
            "filename": API_LOG_PATH,
            "maxBytes": 1e7,
            "backupCount": 100,
        },
    },
    "loggers": {"fastapi": {"level": "INFO", "handlers": ["api_file", "console"]}, "user": {"level": "INFO", "handlers": ["user_file", "console"]}},
}

create_dir(OUTPUT_PATH)
logging.config.dictConfig(logger_config)


def get_fastapi_logger() -> logging.Logger:
    return logging.getLogger("fastapi")


def get_user_logger() -> logging.Logger:
    return logging.getLogger("user")
