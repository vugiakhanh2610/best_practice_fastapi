from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from loguru import logger

from database import get_async_session
from models.user import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from setting import setting
from utils.token_util import load_jwk_kty_EC


async def get_user_db(session = Depends(get_async_session)):
  yield SQLAlchemyUserDatabase(session, User)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
  reset_password_token_secret = 'SECRET'
  verification_token_secret = 'SECRET'
  
  async def on_after_register(self, user: User, request: Optional[Request] = None):
    logger.info(f'User {user.email} has registered.')
    
  async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
    logger.info(f'User {user.email} has forgot their password. Reset token: {token}')
    
  async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
    logger.info(f'Verification requested for user {user.email}. Verification token: {token}')

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
  yield UserManager(user_db)
  
bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')

def get_jwt_strategy() -> JWTStrategy:
  return JWTStrategy(secret=load_jwk_kty_EC(), lifetime_seconds=100*60, algorithm=setting.JWT_ALGORITHM, public_key=load_jwk_kty_EC().public_key())

auth_backend = AuthenticationBackend(
  name='JWT Authentication with Bearer format',
  transport=bearer_transport,
  get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, int](
  get_user_manager=get_user_manager,
  auth_backends=[auth_backend]
)

current_user = fastapi_users.current_user(verified=True, active=True, superuser=True)

def include_auth_router(app: FastAPI):
  app.include_router(
    fastapi_users.get_register_router(UserResponse, UserCreate),
    prefix='/auth'
  )
  app.include_router(
    fastapi_users.get_auth_router(auth_backend, True), prefix='/auth/jwt', tags=['auth']
  )
  app.include_router(
    fastapi_users.get_users_router(UserResponse, UserUpdate),
    prefix='/users',
    tags=['users'],
  )
  app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix='/auth',
    tags=['auth'],
  )
  app.include_router(
    fastapi_users.get_verify_router(UserResponse),
    prefix='/auth',
    tags=['auth'],
  )
