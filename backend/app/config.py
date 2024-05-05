from functools import lru_cache
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    DB_ENGINE: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    model_config = SettingsConfigDict(env_file="app/.env")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
