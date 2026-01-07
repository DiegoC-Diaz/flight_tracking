import os
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from enum import Enum
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("../../.env"))

class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings, extra='ignore'):
    PROJECT_NAME: str = "app"
    BACKEND_CORS_ORIGINS: list[str] | list[AnyHttpUrl]
    MODE: ModeEnum = ModeEnum.development
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    WHEATER_URL: str = "https://wttr.in"
    AIRPORT_DB_TOKEN: str | None = os.getenv("AIRPORT_DB_TOKEN")
    CLIENT_ID: str | None = os.getenv("CLIENT_ID")
    SECRET: str | None =os.getenv
    DATABASE_URL:str = os.getenv("DATABASE_URL")

    
    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("../../.env")


settings = Settings()
