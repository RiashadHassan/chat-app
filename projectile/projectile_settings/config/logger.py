import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
LOG_PATH = os.path.join(BASE_DIR, "projectile_logs")


class DebugOnlyFilter(logging.Filter):
    """Only allows DEBUG level logs"""

    def filter(self, record):
        # Returns True if the record should be logged, or False otherwise.
        return record.levelno == logging.DEBUG


class InfoOnlyFilter(logging.Filter):
    """Only allows INFO level logs"""

    def filter(self, record):
        # Returns True if the record should be logged, or False otherwise.
        return record.levelno == logging.INFO


class ErrorOnlyFilter(logging.Filter):
    """Only allows ERROR level logs"""

    def filter(self, record):
        # Returns True if the record should be logged, or False otherwise.
        return record.levelno == logging.ERROR


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} | {name} | {module} | {funcName} | {lineno} | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "ttl": {
            "format": "[{levelname}] {asctime} | TTL | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",  # allows all since debug is the lowest level
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_PATH, "debug.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filters": ["debug_filter"],  # only DEBUG  logs
        },
        "info_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_PATH, "info.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filters": ["info_filter"],  # only INFO logs
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_PATH, "error.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filters": ["error_filter"],  # only ERROR logs
        },
        "critical_file": {
            "level": "CRITICAL",  # no filter needed since CRITICAL is the highest level
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_PATH, "critical.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "ttl_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_PATH, "ttl.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "ttl",
        },
    },
    "loggers": {
        "ttl": {
            "handlers": ["ttl_file"],
            "level": "INFO",
            "propagate": False,
        }
    },
    # custom log filters
    "filters": {
        # using () to instantiate the filter classes
        "debug_filter": {
            "()": "projectile.projectile_settings.config.logger.DebugOnlyFilter",
        },
        "info_filter": {
            "()": "projectile.projectile_settings.config.logger.InfoOnlyFilter",
        },
        "error_filter": {
            "()": "projectile.projectile_settings.config.logger.ErrorOnlyFilter",
        },
    },
    # add handlers to the root logger for global logging and proper propagation
    "root": {
        "handlers": [
            "console",
            "debug_file",
            "info_file",
            "error_file",
            "critical_file",
        ],
        "level": "DEBUG",
    },
}

# create logs directory if it doesn't exist
os.makedirs(LOG_PATH, exist_ok=True)
