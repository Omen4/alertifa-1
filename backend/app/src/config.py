import sys
import logging
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

from .utils.logging import InterceptHandler


API_PREFIX = "/api"

VERSION = "0.0.0"

config = Config("./src/.env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION", cast=DatabaseURL)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int)

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
ALGORITHM: str = config("ALGORITHM", cast=str)
AUTH_HEADER: str = config("AUTH_HEADER", cast=str)
AUTH_SCHEME: str = config("AUTH_SCHEME", cast=str)
TOKEN_VALIDITY: int = 60 * 24 * 7

PROJECT_NAME: str = config("PROJECT_NAME")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]


logger.configure(handlers=[{"sink": "/logs/app.log", "level": LOGGING_LEVEL}])
# logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
