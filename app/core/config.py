from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.templating import Jinja2Templates

APP_DIR = Path(__name__).resolve().parent


class RunConfig(BaseModel):
    host: str
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(APP_DIR.parent / '.env',),
        env_nested_delimiter='-',
        case_sensitive=False,
        extra = 'allow'
    )
    run: RunConfig
    templates: Jinja2Templates = Jinja2Templates(APP_DIR / 'templates')


settings = Settings()

# print(settings.run.host)
