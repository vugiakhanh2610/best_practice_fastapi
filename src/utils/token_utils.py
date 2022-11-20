from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status

from setting import settings


def create_access_token(subject) -> str:
  payload = {
    'iss': settings.BASE_SERVER_URL,
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_MINUTES),
    'sub': subject,
    'scope': 'access_token'
  }
  encoded_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
  return encoded_jwt

def decode_token(token) -> dict:
  try:
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload
  except(jwt.DecodeError):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Could not validate credentials',
      headers={'WWW-Authenticate': 'Bearer'},
    )
  except(jwt.ExpiredSignatureError):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Token expired',
      headers={'WWW-Authenticate': 'Bearer'},
    )
