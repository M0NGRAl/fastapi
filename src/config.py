from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    DEBUG: bool = True
    TESTING: bool = True

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180
    REFRESH_TOKEN_EXPIRE_DAYS: int = 60

    CORS_ORIGINS: list = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
