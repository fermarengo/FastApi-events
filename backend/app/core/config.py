import secrets

from pydantic import BaseModel, BaseSettings
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="postgres")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

BACKEND_BASE_URL = config("BACKEND_BASE_URL", cast=str)

DEFAULT_EVENT_IMAGES = [
    'back1.jpg',
    'back2.jpg',
    'back3.jpg'
]


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mitin"
    VERSION: str = "1.0.0"
    SECRET_KEY: str = 'OaVTJPt6DC9-A5zCw8IE6dbm27onn8mwgwESTi1ApIcf57RJ3GFh3F4PcyvROX8xzn2wIb-6o5R34Q4oQXgCkw'
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    MEDIA_FOLDER = 'static/'
    BASE_URL = BACKEND_BASE_URL


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    LOGGER_NAME: str = "mitinapp"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "mycoolapp": {"handlers": ["default"], "level": LOG_LEVEL},
    }


settings = Settings()
log_config_settings = LogConfig()
