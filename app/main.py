import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.views import views_router

app = FastAPI()
app.include_router(views_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.run.host, port=settings.run.port)
