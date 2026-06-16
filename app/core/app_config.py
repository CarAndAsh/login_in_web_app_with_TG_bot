import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.templating import Jinja2Templates

APP_DIR = Path(__name__).resolve().parent
LOG_DEFAULT_FORMAT = "APP [%(asctime)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class LogSettings(BaseModel):
    log_level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info'
    log_format: str = LOG_DEFAULT_FORMAT
    log_msec_format: str = '%s.%03d'

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class DBConfig(BaseModel):
    name : str
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 5
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f'sqlite+aiosqlite:///{self.name}'


class ApiPrefix(BaseModel):
    api: str = '/api'
    users: str = '/users'
    auth: str = '/auth'

    @property
    def bearer_token_url(self) -> str:
        return ''.join((self.api,self.auth,'/login')).removeprefix('/')


class RunConfig(BaseModel):
    host: str
    port: int


class JWTStrategySettings(BaseModel):
    secret: str
    lifetime_sec: int = 60


class CookieSettings(BaseModel):
    name: str = 'user-auth'
    max_age: int = 60
    secure: bool = False
    httponly: bool = True
    samesite: Literal['lax', "strict", "none"] = 'lax'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(APP_DIR / '.env',),
        env_nested_delimiter='-',
        case_sensitive=False,
        extra='allow'
    )
    run: RunConfig
    db: DBConfig
    log: LogSettings = LogSettings()
    templates: Jinja2Templates = Jinja2Templates(APP_DIR / 'app' / 'templates')
    api: ApiPrefix = ApiPrefix()
    jwt_strategy: JWTStrategySettings
    cookie: CookieSettings

    @property
    def get_static_dir(self) -> Path: return APP_DIR / 'app' / 'static'

settings = Settings()
