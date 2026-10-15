import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str
    SECRET_KEY: str
    ARGON2_SALT_LENGTH: int = 16
    DATABASE_POOL_SIZE: int = 5


_envSettings = EnvSettings(**{})
envSettings = _envSettings