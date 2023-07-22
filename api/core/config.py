import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
 
# Load environment variables from .env file
load_dotenv()


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    api_debug: bool = True

    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    auth_secret_key: str
    auth_algorithm: str
    auth_access_token_expire_minutes: int

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"