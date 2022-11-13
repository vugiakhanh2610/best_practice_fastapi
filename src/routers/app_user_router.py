import uuid

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.app_user_schema import AppUserCreate, AppUserUpdate
from services.app_user_service import app_user_service
from services.role_service import role_service

router = APIRouter(tags=['app_users'])
RESOURCE = '/app_users'

@cbv(router)
class AppUserRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def create(self, payload: AppUserCreate):
    app_user_service.create(self.session, payload)
    self.session.commit()
    return {'message': 'SUCCESS'}
  
  @router.get(RESOURCE + '/{id}')
  def get_by_id(self, id: uuid.UUID):
    return app_user_service.get_by_id(self.session, id)
  
  def convert_to_CamelCase(self, word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))
    
  @router.put(RESOURCE + '/add_role/{id}')
  def add_role(self, id: uuid.UUID, payload: AppUserUpdate):
    app_user = app_user_service.get_by_id(self.session, id)
    roles_before_update: list = app_user.roles.copy()
    
    for role_id in payload.roles:
      role = role_service.get_by_id(self.session, role_id)
      if role not in roles_before_update:
        app_user.roles.append(role)
      else:
        roles_before_update.remove(role)
    for r in roles_before_update:
      self.session.delete(r)
    self.session.commit()
    return
