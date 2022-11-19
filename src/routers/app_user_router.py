import uuid

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from api_response import APIResponseSuccess
from database import get_session
from schemas.app_user_schema import AppUserCreate, AppUserPassword, AppUserUpdate
from schemas.listing_schema import ListingParams
from services.app_user_service import app_user_service

router = APIRouter(tags=['app_users'])
RESOURCE = '/app_users'

@cbv(router)
class AppUserRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def invite_by_email(self, payload: AppUserCreate):
    app_user = app_user_service.invite_by_email(self.session, payload)
    self.session.commit()
    self.session.refresh(app_user)
    return APIResponseSuccess(data=app_user, message='Please verify your email')
  
  @router.get(RESOURCE + '/{id}')
  def get_by_id(self, id: uuid.UUID):
    data = app_user_service.get_by_id_with_role(self.session, id)
    return APIResponseSuccess(data=data)
  
  @router.put(RESOURCE +'/password/{verify_token}')
  def update_password(self, verify_token: str, payload: AppUserPassword):
    app_user_service.update_password(self.session, verify_token, payload)
    return APIResponseSuccess()
    
  @router.put(RESOURCE + '/add_role/{id}')
  def update(self, id: uuid.UUID, payload: AppUserUpdate):
    app_user_service.update_by_id(self.session, id, payload)
    self.session.commit()
    return APIResponseSuccess()
  
  @router.delete(RESOURCE + '/{id}')
  def delete_by_id(self, id: uuid.UUID):
    app_user_service.delete_by_id(self.session, id)
    self.session.commit()
    return APIResponseSuccess()

  @router.get(RESOURCE)
  def get_list(self, params: ListingParams = Depends(), keyword: str = None):
    query = app_user_service.get_query(self.session, keyword)
    data = app_user_service.get_list(query, params)
    return APIResponseSuccess(data=data)
