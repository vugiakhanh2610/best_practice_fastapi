from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

from database import check_db_info, create_db, create_schema, create_tables
from routers.endpoints import create_endpoints
from security import get_current_user
from setting import Settings, get_settings, settings


def include_router(app: FastAPI):
  logger.debug('Including Routers')
  create_endpoints(app)
  
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

@app.exception_handler(HTTPException)
def http_exception_handler(request, exception: HTTPException):
  return JSONResponse(
    status_code = exception.status_code,
    content = {
      'message': HTTPStatus(exception.status_code).phrase,
      'error_details': exception.detail,
      'data': None
    }
  ) 

@app.get('/info', tags=['Info'], description='Full information of project', )
def get_info_project(settings: Settings = Depends(get_settings), current_user = Depends(get_current_user)):
  return settings.dict()

@app.on_event('startup')
async def app_startup():
  logger.debug("Checking database's information")
  await check_db_info()

@app.on_event('shutdown')
def app_shutdown():
  # truncate_db()
  pass

  
