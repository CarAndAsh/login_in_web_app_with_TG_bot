import logging
from logging import Formatter
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict

BOT_DIR = Path(__name__).resolve().parent.parent
BASE_DIR = BOT_DIR.parent

LOG_DEFAULT_FORMAT = '{levelname}\t[{asctime}]\t{name}: {lineno}\t{filename}\t{message}'


class LogConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    log_level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info'
    formatter: Formatter = Formatter(fmt=LOG_DEFAULT_FORMAT, style='{')

    @property
    def get_log_lvl(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level]


class RegBotConfig(BaseModel):
    token: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_nested_delimiter='-',
        extra='ignore'
    )
    log: LogConfig = LogConfig()
    reg_bot: RegBotConfig


settings = Settings()
