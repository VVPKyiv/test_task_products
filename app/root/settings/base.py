import secrets
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class SettingsBase(BaseSettings):
    API_V1_STR: str
    SECRET_KEY: str
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: str
    JSON_FILE_PATH: Optional[str]
    S3_CLIENT: Optional[str]


def get_settings():
    return SettingsBase()
