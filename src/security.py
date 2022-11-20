from functools import wraps
from http import HTTPStatus

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_session
from models.app_user import AppUser
from models.group import Group
from services.app_user_service import app_user_service
from utils.token_utils import decode_token

#########################################################################################
#
# Authentication
#
#########################################################################################

class UserSession:
  def __init__(self, user_info, session):
    self.user_info: AppUser = user_info
    self.session: Session   = session
    
    # @event.listens_for(Base, 'before_insert', propagate=True)
    # def before_insert(mapper, connect, target):
    #   if (hasattr(target, 'deleted')):
    #     target.deleted = False
    #   target.created_by = user_info.username
    #   target.created_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    
    # @event.listens_for(Base, 'before_update', propagate=True)
    # def before_update(mapper, connect, target):
    #   target.updated_by = user_info.username
    #   target.updated_time = datetime.utcnow().replace(tzinfo=timezone.utc)

auth_scheme = HTTPBearer()

async def get_current_user(data: HTTPAuthorizationCredentials = Depends(auth_scheme), session: Session = Depends(get_session)) -> AppUser:
  payload = decode_token(data.credentials)
  app_user = app_user_service.get_by_id_with_group(session, payload['sub'])
  yield UserSession(app_user, session)

#########################################################################################
#
# Permission
#
#########################################################################################

def auth_check(required_roles: list[str]):
  def decorator_auth(func):
    @wraps(func)
    def wrapper_auth(*args, **kwargs):
      self = kwargs['self']
      current_user = self.current_user.user_info
      print(current_user)
      request: Request = kwargs['request']
      http_method = request.method
      print(http_method)
      group: Group = current_user.group
      
      if http_method == 'GET':
        for module_permission in group.module_permissions:
          if module_permission.module.name in required_roles:
            if module_permission.read:
              return func(*args, **kwargs)
      elif http_method == 'POST':
        for module_permission in group.module_permissions:
          if module_permission.module.name in required_roles:
            if module_permission.create:
              return func(*args, **kwargs)
      elif http_method == 'PUT':
        for module_permission in group.module_permissions:
          if module_permission.module.name in required_roles:
            if module_permission.update:
              return func(*args, **kwargs)
      else:
        for module_permission in group.module_permissions:
          if module_permission.module.name in required_roles:
            if module_permission.delete:
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
