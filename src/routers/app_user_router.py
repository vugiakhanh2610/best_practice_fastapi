import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from pydantic import EmailStr
from sqlalchemy.orm import Session

from database import get_session
from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.app_user_schema import (AppUserCreate, AppUserPassword, AppUserResponse, AppUserResponsePage, AppUserToken, AppUserUpdate)
from schemas.listing_schema import ListingParams
from security import UserSession, auth_check, get_current_user
from services.app_user_service import app_user_service

RESOURCE = 'app_users'
router = APIRouter(tags=[RESOURCE])

@cbv(router)
class AppUserRouter:
  
  current_user: UserSession = Depends(get_current_user)
  
  @router.post(f'/{RESOURCE}')
  @auth_check([RESOURCE])
  def invite_by_email(self, request: Request, payload: AppUserCreate):
    app_user = app_user_service.invite_by_email(self.current_user.session, payload)
    self.current_user.session.commit()
    self.current_user.session.refresh(app_user)
    return APIResponse(data=jsonable_encoder(app_user), message=f'Please verify email {payload.email}')
  
  @router.get(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def get_by_id(self, request: Request, id: uuid.UUID):
    data = app_user_service.get_by_id_with_group(self.current_user.session, id)
    return APIResponse[AppUserResponse](data=jsonable_encoder(data))
  
  @router.put(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def update(self, request: Request, id: uuid.UUID, payload: AppUserUpdate):
    app_user_service.update_by_id(self.current_user.session, id, payload)
    self.current_user.session.commit()
    return APIResponse()
  
  @router.delete(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def delete_by_id(self, request: Request, id: uuid.UUID):
    app_user_service.delete_by_id(self.current_user.session, id)
    self.current_user.session.commit()
    return APIResponse()

  @router.get(f'/{RESOURCE}')
  @auth_check([RESOURCE])
  def get_list(
    self,
    request: Request,
    params: ListingParams = Depends(),
    keyword: str = None
  ):
    query = app_user_service.get_query(self.current_user.session, keyword)
    data = app_user_service.get_list(query, params)
    return APIResponse[PaginatedData[AppUserResponsePage]](data=data)
  

@cbv(router)
class UnauthenticatedRouter:
  
  session: Session = Depends(get_session)
  
  @router.put(f'/{RESOURCE}' +'/password/{verify_token}')
  def reset_password(self, verify_token: str, payload: AppUserPassword):
    app_user_service.reset_password(self.session, verify_token, payload)
    self.session.commit()
    return APIResponse()
  
  @router.get(f'/{RESOURCE}' + '/verify_token/{email}')
  def forgot_password(self, email: EmailStr):
    verify_token = app_user_service.forgot_password(self.session, email)
    self.session.commit()
    return APIResponse[AppUserToken](data=AppUserToken(token=verify_token), message='Please use this token to reset password')
