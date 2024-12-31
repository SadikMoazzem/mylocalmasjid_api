import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "My Local Masjid API"
    VERSION: str = "4.0.0"
    DESCRIPTION: str = "API for My Local Masjid"
    ENV: Literal["development", "staging", "production"] = os.getenv("API_ENV", "development")
    DATABASE_URI: str =  os.getenv("DATABASE_URL", "not_set")
    SECRET_KEY: str =  os.getenv("SECRET_KEY", "not_so_secret")
    ACCESS_TOKEN_EXPIRE: int = 1800 # seconds (30 minutes)
    REFRESH_TOKEN_EXPIRE: int = 604800 # seconds (7 days)

    class Config:
        case_sensitive = True


settings = Settings()
