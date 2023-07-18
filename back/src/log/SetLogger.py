import logging
import logging.config
from . import CreateDirectory

OUTPUT_PATH = "outputs/logs"
LOG_PATH = OUTPUT_PATH + "/userlog.log"

logger_config = {
    "version" : 1,
    "disable_existing_loggers": True,
    "formatters" :{
        "basic" : {"format" : "%(asctime)s | %(levelname)s - %(message)s"}
    },
    "handlers" : {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter" : "basic"
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "mode": "a",
            "formatter" : "basic",
            "filename": LOG_PATH,
            "encoding": "UTF-8",
            "maxBytes": 1e7,
            "backupCount": 100
        }
    },
    "loggers": {"fastapi":{"level": "INFO", "handlers":["file", "console"]}}
}


def setLogger() -> logging.Logger:
    CreateDirectory.createDirectory(OUTPUT_PATH)
    logging.config.dictConfig(logger_config)
    return logging.getLogger("fastapi")
