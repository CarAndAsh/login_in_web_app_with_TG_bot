from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

APP_DIR = Path(__name__).resolve().parent.parent

class RunConfig(BaseModel):
    host: str
    port: int

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(APP_DIR / '.env',),
        env_nested_delimiter='-',
        case_sensitive=False,
    )
    run: RunConfig

settings = Settings()

# print(settings.run.host)
