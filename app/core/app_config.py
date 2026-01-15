import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.templating import Jinja2Templates

APP_DIR = Path(__name__).resolve().parent
LOG_DEFAULT_FORMAT = "[%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class LogSettings(BaseModel):
    log_level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT
    log_msec_format: str = '%s.%03d'

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RunConfig(BaseModel):
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(APP_DIR / '.env',),
        env_nested_delimiter='-',
        case_sensitive=False,
        extra='allow'
    )
    run: RunConfig
    log: LogSettings = LogSettings()
    templates: Jinja2Templates = Jinja2Templates(APP_DIR / 'app' / 'templates')


settings = Settings()
