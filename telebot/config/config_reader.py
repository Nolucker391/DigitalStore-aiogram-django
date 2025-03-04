from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    model_config: ClassVar[SettingsConfigDict] = {
        # "env_file": ".env",
        "env_file": "bot/config/.env",
        "env_file_encoding": "utf-8"
    }

config = Settings()