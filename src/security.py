from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_session
from models.app_user import AppUser
from services.app_user_service import app_user_service
from utils.token_utils import decode_token

auth_scheme = HTTPBearer()

async def get_current_user(data: HTTPAuthorizationCredentials = Depends(auth_scheme), session: Session = Depends(get_session)) -> AppUser:
  payload = decode_token(data.credentials)
  app_user = app_user_service.get_by_id(session, payload['sub'])
  return app_user
