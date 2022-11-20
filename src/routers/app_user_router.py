import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from pydantic import EmailStr
from sqlalchemy.orm import Session

from database import get_session
from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.app_user_schema import (AppUserCreate, AppUserPassword, AppUserResponse, AppUserResponsePage, AppUserUpdate)
from schemas.listing_schema import ListingParams
from security import auth_check, get_current_user
from services.app_user_service import app_user_service

router = APIRouter(tags=['app_users'])
RESOURCE = '/app_users'

@cbv(router)
class AppUserRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def invite_by_email(self, request: Request, payload: AppUserCreate, current_user = Depends(get_current_user)):
    app_user = app_user_service.invite_by_email(self.session, payload)
    self.session.commit()
    self.session.refresh(app_user)
    return APIResponse(data=jsonable_encoder(app_user), message=f'Please verify email {payload.email}')
  
  @router.get(RESOURCE + '/{id}')
  @auth_check(['user'])
  def get_by_id(self, request: Request, id: uuid.UUID, current_user = Depends(get_current_user)):
    data = app_user_service.get_by_id_with_role(self.session, id)
    return APIResponse[AppUserResponse](data=jsonable_encoder(data))
  
  @router.get(RESOURCE + '/verify_token/{email}')
  def forgot_password(self, email: EmailStr):
    verify_token = app_user_service.forgot_password(self.session, email)
    self.session.commit()
    return APIResponse(data=verify_token, message='Please use this token to reset password')
  
  @router.put(RESOURCE +'/password/{verify_token}')
  def reset_password(self, verify_token: str, payload: AppUserPassword):
    app_user_service.reset_password(self.session, verify_token, payload)
    self.session.commit()
    return APIResponse()
    
  @router.put(RESOURCE + '/add_role/{id}')
  def update(self, request: Request, id: uuid.UUID, payload: AppUserUpdate, current_user = Depends(get_current_user)):
    app_user_service.update_by_id(self.session, id, payload)
    self.session.commit()
    return APIResponse()
  
  @router.delete(RESOURCE + '/{id}')
  def delete_by_id(self, request: Request, id: uuid.UUID, current_user = Depends(get_current_user)):
    app_user_service.delete_by_id(self.session, id)
    self.session.commit()
    return APIResponse()

  @router.get(RESOURCE)
  def get_list(
    self,
    request: Request,
    params: ListingParams = Depends(),
    keyword: str = None,
    current_user = Depends(get_current_user)
  ):
    query = app_user_service.get_query(self.session, keyword)
    data = app_user_service.get_list(query, params)
    return APIResponse[PaginatedData[AppUserResponsePage]](data=data)
