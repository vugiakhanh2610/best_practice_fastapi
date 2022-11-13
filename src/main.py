from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger

from api_response import APIResponseError
from database import create_db, create_schema, create_tables
from routers.endpoints import create_endpoints
from setting import settings


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
    content = jsonable_encoder(
      APIResponseError(
        message = HTTPStatus(exception.status_code).phrase,
        error_details = exception.detail
      )
    )
  ) 

# @app.get('/info', tags=['Info'], description='Full information of project', )
# def get_info_project(settings: Settings = Depends(get_settings), credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(), use_cache=False)):
#   token = credentials.credentials
#   decode_token(token)
#   return settings.dict()

@app.on_event('startup')
async def app_startup():
  logger.debug("Checking database's information")
  # await check_db_info()

@app.on_event('shutdown')
def app_shutdown():
  # truncate_db()
  pass

  
