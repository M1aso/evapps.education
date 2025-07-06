from pydantic import BaseSettings

class Settings(BaseSettings):
    analytics_database_url: str
    rabbitmq_url: str
    log_level: str = "info"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_prefix = ""

def get_settings() -> Settings:
    return Settings()
