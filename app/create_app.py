from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import Server, Config

from app.api import api_router
from app.core.app_log_cofig import app_logger
from app.core.app_config import settings
from app.models import db_helper
from app.views import views_router

app_logger.name = __file__




async def start_web_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        await db_helper.dispose()

    app = FastAPI(lifespan=lifespan)
    app.include_router(views_router)
    app.include_router(api_router)

    app_logger.debug('Приложение запущено')
    server_config = Config(app, host=settings.run.host, port=settings.run.port)
    app_server = Server(server_config)
    await app_server.serve()
