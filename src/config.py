from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

path = Path.joinpath(Path(__file__).parent.parent, ".env")


class Settings(BaseSettings):
    api_key: str

    class Config:
        env_file = path


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
