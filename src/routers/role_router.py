import uuid

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.role_schema import RoleCreate
from services.role_service import role_service

router = APIRouter(tags=['roles'])
RESOURCE = '/roles'

@cbv(router)
class AppUserRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def create(self, payload: RoleCreate):
    role_service.create(self.session, payload)
    self.session.commit()
    return {'message': 'SUCCESS'}
  
  @router.get(RESOURCE + '/{id}')
  def get_by_id(self, id: uuid.UUID):
    return role_service.get_by_id(self.session, id)
    
  # @router.get()
