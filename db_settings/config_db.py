import os
from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv()

config_dict = {
    "DB_HOST": os.environ.get("DB_HOST"),
    "DB_PORT": os.environ.get("DB_PORT"),
    "DB_USER": os.environ.get("DB_USER"),
    "DB_PASS": os.environ.get("DB_PASS"),
    "DB_NAME": os.environ.get("DB_NAME"),
}


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Подключаем данные из файла .env
    model_config = SettingsConfigDict(config_dict)
    # model_config = SettingsConfigDict(env_prefix='DB_', env_file=BASE_DIR.joinpath('.env'))


settings = Settings()
