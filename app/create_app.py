from contextlib import asynccontextmanager
from logging import getLogger, config as logger_config

from fastapi import FastAPI
from uvicorn import Server, Config

from app.api import api_router
from app.core.app_config import settings
from app.core.app_log_cofig import log_config_dict
from app.models import db_helper
from app.views import views_router



async def start_web_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        lifespan_app_log = getLogger(__name__)
        logger_config.dictConfig(log_config_dict)
        yield
        await db_helper.dispose()

    app = FastAPI(lifespan=lifespan)
    app.include_router(views_router)
    app.include_router(api_router)

    server_config = Config(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
    app_server = Server(server_config)

    await app_server.serve()
