import secrets
import uuid

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session, eagerload

from enums.sendgrid_enum import TemplateId
from models.app_user import AppUser
from schemas.app_user_schema import AppUserCreate, AppUserPassword, AppUserUpdate
from services.base_service import CRUDBaseService
from services.sendgrid_service import get_payload, send_email
from utils.hashing_util import get_hashed_obj
from utils.helper_utils import set_value


class AppUserService(CRUDBaseService[AppUserCreate, AppUserUpdate, AppUser]):
  def get_by_email(self, session: Session, email: EmailStr) -> AppUser:
    return session.query(AppUser).filter(AppUser.email == email).first()
  
  def invite_by_email(self, session: Session, payload: AppUserCreate):
    app_user = self.get_by_email(session, payload.email)
    if not app_user:
      app_user = AppUser()
    elif app_user.is_verified:
      raise HTTPException(status_code=409, detail='Email already verified')
    set_value(app_user, payload, {'roles'})
    app_user.is_verified = False
    
    # Generate one-time token and save into database
    token = secrets.token_urlsafe(32)
    app_user.verify_token = token
    session.add(app_user)
    
    template_id = TemplateId.USER_INVITATION_TEMPLATE.value
    data = {
      'subject': 'Invite to CarBuyer Admin portal',
      'username': payload.username,
      'link': f'http://localhost:10001/docs#/app_users/update_password_api_v1_app_users_password__verify_token__put/{token}'
    }
    payload = get_payload(email_to=[payload.email], template_id=template_id, data=data)
    send_email(payload)
    
    return app_user
  
  def get_by_verify_token(self, session: Session, verify_token: str) -> AppUser:
    return session.query(AppUser).filter(AppUser.verify_token == verify_token).one()
  
  def forgot_password(self, session: Session, email: EmailStr):
    app_user = self.get_by_email(session, email)
    if not app_user:
      raise HTTPException(status_code=404, detail='User with this email not exists')
    token = secrets.token_urlsafe(32)
    app_user.verify_token = token
    return token

  def reset_password(self, session: Session, verify_token: str, payload: AppUserPassword):
    app_user = self.get_by_verify_token(session, verify_token)
    app_user.is_verified = True
    app_user.verify_token = None
    hashed_password = get_hashed_obj(payload.password)
    app_user.password = hashed_password
    return
  
  def update_by_id(self, session: Session, id: uuid.UUID, payload: AppUserUpdate):
    app_user = self.get_by_id(session, id)
    set_value(app_user, payload)
    # roles_before_update: list = app_user.roles.copy()
    # for role_id in payload.roles:
    #   role = role_service.get_by_id(session, role_id)
    #   if role not in roles_before_update:
    #     app_user.roles.append(role)
    #   else:
    #     roles_before_update.remove(role)
    # for r in roles_before_update:
    #   app_user.roles.remove(r)
    return
  
  def get_query(self, session: Session, keyword: str = None):
    condition = []
    # Search
    if keyword:
      condition.append(
        AppUser.email.ilike(f'%{keyword}%')
        | AppUser.username.ilike(f'%{keyword}%')
      )
    return super().get_query(session, condition)
  
  def get_list(
    self,
    query,
    params,
  ):
    return super().get_list(query, params)
  
  def get_by_id_with_group(self, session: Session, id: uuid.UUID):
    return jsonable_encoder(session.query(AppUser).options(eagerload(AppUser.group)).filter(AppUser.id == id).one())
  
app_user_service = AppUserService(AppUser)
