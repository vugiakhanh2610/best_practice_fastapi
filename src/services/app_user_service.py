import secrets

from sqlalchemy.orm import Session

from enums.sendgrid_enum import TemplateId
from models.app_user import AppUser
from schemas.app_user_schema import AppUserCreate, AppUserPassword, AppUserResponse, AppUserUpdate
from services.base_service import CRUDBaseService
from services.sendgrid_service import get_payload, send_email
from utils.hashing_util import hash_obj
from utils.helper_utils import set_value


class AppUserService(CRUDBaseService[AppUserCreate, AppUserUpdate, AppUserResponse]):
  def create(self, session: Session, payload: AppUserCreate):
    app_user = AppUser()
    set_value(app_user, payload, {'roles'})
    app_user.is_verified = False
    
    # Generate one-time token and save into database
    token = secrets.token_urlsafe(32)
    app_user.verify_token = token
    session.add(app_user)
    session.commit()
    session.refresh(app_user)
    
    template_id = TemplateId.USER_INVITATION_TEMPLATE.value
    data = {
      'subject': 'Invite to CarBuyer Admin portal',
      'username': payload.username,
      'link': f'http://localhost:10001/docs#/app_users/reset_password_api_v1_app_users_reset_password__verify_token__put/{token}'
    }
    payload = get_payload(email_to=[payload.email], template_id=template_id, data=data)
    send_email(payload)
    
    return app_user
  
  def get_by_verify_token(self, session: Session, verify_token: str) -> AppUser:
    return session.query(AppUser).filter(AppUser.verify_token == verify_token).one()

  def reset_password(self, session: Session, verify_token: str, payload: AppUserPassword):
    app_user = self.get_by_verify_token(session, verify_token)
    app_user.verify_token = None
    hashed_password = hash_obj(payload.password)
    app_user.password = hashed_password
    session.commit()
    return
    
  
app_user_service = AppUserService(AppUser)
