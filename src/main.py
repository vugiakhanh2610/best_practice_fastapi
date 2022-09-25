from functools import lru_cache

from fastapi import Depends, FastAPI, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger

from database import check_db_info, create_db, create_schema, create_tables
from routers import user_router
from setting import Setting, setting
from utils.token_util import decode_token


# https://fastapi.tiangolo.com/es/advanced/settings/
@lru_cache()
def get_setting():
  return setting

def include_router(app: FastAPI):
  logger.debug('Including Routers')
  app.include_router(user_router.router)
  
def start_application():
  app = FastAPI(
    title = setting.PROJECT_NAME,
    version = setting.PROJECT_VERSION,
    contact = setting.PROJECT_OWNER
  )
  create_db()
  create_schema()
  create_tables()
  include_router(app)
  return app

app = start_application()

@app.get('/info', tags=['Info'], description='Full information of project', )
def get_info_project(setting: Setting = Depends(get_setting), credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(), use_cache=False)):
  token = credentials.credentials
  decode_token(token)
  return setting.dict()

@app.on_event('startup')
async def app_startup():
  logger.debug("Checking database's information")
  await check_db_info()

@app.on_event('shutdown')
def app_shutdown():
  # truncate_db()
  pass
  
