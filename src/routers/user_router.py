from abc import ABC
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.user_schema import UserCreate
from services.user_service import UserService

router = APIRouter(prefix='/api/v1/user')
@cbv(router)
class UserRouter:
  
  session: Session = Depends(get_session)

  @router.get('')
  def get_all(self):
    return UserService.get_all(self.session)

  @router.get('/{id}')
  def get_by_id(self, id: int):
    return UserService.get_by_id(self.session, id)
  
  @router.post('')
  def create_user(self, payload: UserCreate):
    return UserService.create(self.session, payload)

  @router.put('')
  def update(self, id: int, payload: UserCreate):
    return UserService.update(self.session, id, payload)
  
  @router.delete('')
  def delete_by_id(self, id: int):
    return UserService.delete_by_id(self.session, id)