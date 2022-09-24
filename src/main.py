from functools import lru_cache

from fastapi import Depends, FastAPI
from loguru import logger

from database import Base, check_db_info, engine
from routers import user_router
from setting import Setting

setting = Setting()
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
    title = setting.PROJECT_NAME,
    version = setting.PROJECT_VERSION,
    contact = setting.PROJECT_OWNER
  )
  create_table()
  include_router(app)
  return app

app = start_application()

@app.get('/info', tags=['Info'], description='Full information of project')
def get_info_project(setting: Setting = Depends(get_setting)):
  return setting.dict()

@app.on_event('startup')
async def app_startup():
  logger.debug("Checking database's information")
  await check_db_info()

  
