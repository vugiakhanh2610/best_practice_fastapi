import base64
import json
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from jwt.algorithms import ECAlgorithm

from setting import settings


def load_jwk_kty_EC():
  algorithm = ECAlgorithm(f'{settings.JWT_ALGORITHM}')
  key = settings.ES256_KEY
  decoded_key = base64.b64decode(key)
  json_decoded_key = json.loads(decoded_key)
  return algorithm.from_jwk(json_decoded_key['keys'][0])
  
def generate_token(email):
  payload = {
    'iss': settings.BASE_SERVER_URL,
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRY_IN_MINUTES),
    'sub': email,
    'scope': 'access_token'
  }
  signing_key = load_jwk_kty_EC()
  return jwt.encode(payload, signing_key, settings.JWT_ALGORITHM, headers={'kid': settings.ES256_KID})
  
def decode_token(token):
  try:
    public_key = load_jwk_kty_EC().public_key()
    decoded_token = jwt.decode(token, public_key, settings.JWT_ALGORITHM)
    return decoded_token
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token', headers={'WWW-Authenticate': 'Bearer'})
    
