from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr
    ENDPOINT_URL: SecretStr
    model_config = SettingsConfigDict(env_file="bot/.env", env_file_encoding="utf-8")


config = Settings()
