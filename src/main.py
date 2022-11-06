from fastapi import Depends, FastAPI
from loguru import logger

from database import check_db_info, create_db, create_schema, create_tables
from models.user import User
from security.secure import current_user, include_auth_router
from setting import settings


def include_router(app: FastAPI):
  logger.debug('Including Routers')
  include_auth_router(app)
  
def start_application():
  app = FastAPI(
    title = settings.PROJECT_NAME,
    version = settings.PROJECT_VERSION,
    contact = settings.PROJECT_OWNER
  )
  create_db()
  create_schema()
  create_tables()
  include_router(app)
  return app

app = start_application()

@app.get('/info', tags=['Info'], description='Full information of project', )
def get_info_project(user: User = Depends(current_user)):
  return settings.dict()

# @app.get('/info', tags=['Info'], description='Full information of project', )
# def get_info_project(settings: Settings = Depends(get_settings), credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(), use_cache=False)):
#   token = credentials.credentials
#   decode_token(token)
#   return settings.dict()

@app.on_event('startup')
async def app_startup():
  logger.debug("Checking database's information")
  await check_db_info()

@app.on_event('shutdown')
def app_shutdown():
  # truncate_db()
  pass

  
