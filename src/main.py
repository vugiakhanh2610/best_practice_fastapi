import uvicorn
from fastapi import FastAPI
from loguru import logger

from config.core import Setting
from database import Base, engine

from routers import user_router


def create_table():
  logger.debug('Creating Tables')
  Base.metadata.create_all(bind=engine, checkfirst=True)
  
def include_router(app: FastAPI):
  logger.debug('Including Routers')
  app.include_router(user_router.router)
  
def start_application():
  app = FastAPI(
    title = Setting.PROJECT_NAME,
    version = Setting.PROJECT_VERSION
  )
  create_table()
  include_router(app)

  return app

app = start_application()

  