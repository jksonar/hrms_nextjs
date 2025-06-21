import os
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'.env.{os.getenv("APP_ENV", "dev")}')

    PROJECT_NAME: str = "HRMS API"
    API_V1_STR: str = "/api/v1"

    APP_ENV: str = "dev"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080
    ADMIN_EMAIL: str = "admin@example.com"
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]


settings = Settings()