from functools import wraps
from http import HTTPStatus

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_session
from models.app_user import AppUser
from services.app_user_service import app_user_service
from utils.token_utils import decode_token

auth_scheme = HTTPBearer()

async def get_current_user(data: HTTPAuthorizationCredentials = Depends(auth_scheme), session: Session = Depends(get_session)) -> AppUser:
  payload = decode_token(data.credentials)
  app_user = app_user_service.get_by_id(session, payload['sub'])
  return app_user

def auth_check(required_roles):
  def decorator_auth(func):
    @wraps(func)
    def wrapper_auth(*args, **kwargs):
      request: Request = kwargs['request']
      http_method = request.method
      print(http_method)
      current_user = kwargs['current_user']
      group = current_user.group
      for role in group.modules:
        if role.name in required_roles:
          return func(*args, **kwargs)
      return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
          'error_details': None,
          'message': HTTPStatus(403).phrase,
          'detail': 'Not allowed to access this resource'
        }
      )
        
    return wrapper_auth
  return decorator_auth
