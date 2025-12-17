import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    
    DATABASE_URL: str = "sqlite:///portfolio.db"
    
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "changeme"
    SECRET_KEY: str = "change-this-in-production-use-openssl-rand-hex-32"
    
    CORS_ORIGINS: list[str] = ["https://doazhu.pro", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

