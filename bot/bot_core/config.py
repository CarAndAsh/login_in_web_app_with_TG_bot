from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

import logging

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DEFAULT_FORMAT = "[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class LogSettings(BaseModel):
    log_level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT
    log_msec_format: str = '%s.%03d'

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class TGBotSettings(BaseModel):
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_nested_delimiter='-',
        case_sensitive=False,
        extra='ignore'
    )
    tg_bot: TGBotSettings
    log: LogSettings = LogSettings()


settings = Settings()
