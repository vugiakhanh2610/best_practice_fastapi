from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from services.app_user_service import app_user_service
from utils.hashing_util import verify_hashed_obj
from utils.token_utils import create_access_token

router= APIRouter(tags=['authentication'])

@cbv(router)
class AuthRouter:
  
  session: Session = Depends(get_session)
  
  @router.post('/login')
  def login(self, credentials: OAuth2PasswordRequestForm = Depends()):
    app_user = app_user_service.get_by_email(self.session, credentials.username)
    if not app_user:
      raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not app_user.is_verified:
      raise HTTPException(status_code=400, detail='Please verify your email')
    elif not verify_hashed_obj(credentials.password, app_user.password):
      raise HTTPException(status_code=400, detail='Incorrect email or password')
    return create_access_token(jsonable_encoder(app_user.id))
  
