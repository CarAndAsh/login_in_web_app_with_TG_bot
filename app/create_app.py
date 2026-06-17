from contextlib import asynccontextmanager
from logging import getLogger, config as logger_config

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from uvicorn import Server, Config

from app.api import api_router
from app.core.app_config import settings
from app.core.app_log_cofig import log_config_dict
from app.models import db_helper
from app.views import views_router
from app.views.error_handler import register_errors_handlers


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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=('http://127.0.0.1:8000/','http://localhost:8000/' ),
        allow_methods='*',
        allow_credentials=True,
    )
    app.mount('/static', app=StaticFiles(directory=settings.get_static_dir), name='static')
    server_config = Config(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
    app_server = Server(server_config)
    register_errors_handlers(app)

    await app_server.serve()
