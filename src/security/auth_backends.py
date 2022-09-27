from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from setting import settings
from utils.token_util import load_jwk_kty_EC

bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

def get_jwt_strategy() -> JWTStrategy:
  return JWTStrategy(secret=load_jwk_kty_EC(), lifetime_seconds=100*60, algorithm=settings.JWT_ALGORITHM, public_key=load_jwk_kty_EC().public_key())

jwt_auth_backend = AuthenticationBackend(
  name='JWT Authentication with Bearer format',
  transport=bearer_transport,
  get_strategy=get_jwt_strategy
)
