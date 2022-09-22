from fastapi import FastAPI, Depends
from functools import lru_cache
from loguru import logger

from setting import Setting
from database import Base, engine

from routers import user_router

# https://fastapi.tiangolo.com/es/advanced/settings/
@lru_cache()
def get_setting():
  return Setting()

def create_table():
  logger.debug('Creating Tables')
  Base.metadata.create_all(bind=engine, checkfirst=True)
  
def include_router(app: FastAPI):
  logger.debug('Including Routers')
  app.include_router(user_router.router)
  
def start_application():
  app = FastAPI(
    title = Setting().PROJECT_NAME,
    version = Setting().PROJECT_VERSION,
    contact = Setting().PROJECT_OWNER
  )
  create_table()
  include_router(app)
  return app

app = start_application()

@app.get('/info', tags=['Info'], description='Full information of project')
def get_info_project(setting: Setting = Depends(get_setting)):
  return setting.dict()

  