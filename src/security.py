from datetime import datetime, timezone
from functools import wraps

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import event
from sqlalchemy.orm import Session

from database import Base, get_session
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
    
    @event.listens_for(Base, 'before_insert', propagate=True)
    def before_insert(mapper, connect, target):
      target.created_by = self.user_info.email
      target.created_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    
    @event.listens_for(Base, 'before_update', propagate=True)
    def before_update(mapper, connect, target):
      target.updated_by = self.user_info.email
      target.updated_time = datetime.utcnow().replace(tzinfo=timezone.utc)

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
      group: Group = current_user.group
      
      if not group:
        raise HTTPException(status_code=403, detail='Access denied')
      
      request: Request = kwargs['request']
      http_method = request.method
      
      for module_permission in group.module_permissions:
        if module_permission.module.name in required_roles:
          if (
            (http_method == 'GET' and module_permission.read)
            or (http_method == 'POST' and module_permission.create)
            or (http_method == 'PUT' and module_permission.update)
            or (http_method == 'DELETE' and module_permission.delete)
          ):
            return func(*args, **kwargs)
      raise HTTPException(status_code=403, detail='Access denied')
        
    return wrapper_auth
  return decorator_auth
