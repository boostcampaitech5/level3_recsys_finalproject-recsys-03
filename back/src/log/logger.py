import logging
import logging.config
from ..utils import create_dir


OUTPUT_PATH = "outputs/logs"
USER_LOG_PATH = OUTPUT_PATH + "/user_log.log"
FEEDBACK_LOG_PATH = OUTPUT_PATH + "/feedback_log.log"
SPOTIFY_LOG_PATH = OUTPUT_PATH + "/spotify_log.log"
API_LOG_PATH = OUTPUT_PATH + "/api_log.log"

logger_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "basic": {"format": "%(asctime)s | %(levelname)s - %(message)s"},
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(filename)s",
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
        "feedback_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter": "basic",
            "encoding": "utf-8",
            "filename": FEEDBACK_LOG_PATH,
            "maxBytes": 1e7,
            "backupCount": 100,
        },
        "spotify_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter": "basic",
            "encoding": "utf-8",
            "filename": SPOTIFY_LOG_PATH,
            "maxBytes": 1e7,
            "backupCount": 100,
        },
    },
    "loggers": {
        "fastapi": {"level": "INFO", "handlers": ["api_file", "console"]},
        "user": {"level": "INFO", "handlers": ["user_file", "console"]},
        "feedback": {"level": "INFO", "handlers": ["feedback_file", "console"]},
        "spotify": {"level": "INFO", "handlers": ["spotify_file"]},
    },
}

create_dir(OUTPUT_PATH)
logging.config.dictConfig(logger_config)


def get_fastapi_logger() -> logging.Logger:
    return logging.getLogger("fastapi")


def get_user_logger() -> logging.Logger:
    return logging.getLogger("user")


def get_feedback_logger() -> logging.Logger:
    return logging.getLogger("feedback")


def get_spotify_logger() -> logging.Logger:
    return logging.getLogger("spotify")
