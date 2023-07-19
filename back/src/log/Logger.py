import logging
import logging.config
from src.utils import create_dir

OUTPUT_PATH = "outputs/logs"
USER_LOG_PATH = OUTPUT_PATH + "/user_log.log"
API_LOG_PATH = OUTPUT_PATH + "/api_log.log"

logger_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {"basic": {"format": "%(asctime)s | %(levelname)s - %(message)s"}},
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "basic"},
        "user_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter": "basic",
            "filename": USER_LOG_PATH,
            "encoding": "UTF-8",
            "maxBytes": 1e7,
            "backupCount": 100,
        },
        "api_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter": "basic",
            "filename": API_LOG_PATH,
            "encoding": "UTF-8",
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
