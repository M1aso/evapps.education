import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("AUTH_DATABASE_URL", "sqlite:///./auth.db")
    jwt_secret: str = os.getenv("JWT_SECRET", "secret")
    access_token_ttl: int = 3600  # 1h
    refresh_token_ttl: int = 30 * 24 * 3600  # 30d

settings = Settings()
