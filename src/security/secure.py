from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from models.user import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from security.auth_backends import jwt_auth_backend
from security.user_manager import get_user_manager

AUTH_PREFIX = '/auth'

fastapi_users = FastAPIUsers[User, int](
  get_user_manager=get_user_manager,
  auth_backends=[jwt_auth_backend]
)

current_user = fastapi_users.current_user(verified=True, active=True, superuser=True)

def include_auth_router(app: FastAPI):
  app.include_router(
    fastapi_users.get_register_router(UserResponse, UserCreate),
    prefix=AUTH_PREFIX,
    tags=['auth'],
  )
  app.include_router(
    fastapi_users.get_auth_router(jwt_auth_backend, True), prefix='/auth/jwt', tags=['auth']
  )
  app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=AUTH_PREFIX,
    tags=['auth'],
  )
  app.include_router(
    fastapi_users.get_verify_router(UserResponse),
    prefix=AUTH_PREFIX,
    tags=['auth'],
  )
  app.include_router(
    fastapi_users.get_users_router(UserResponse, UserUpdate),
    prefix='/users',
    tags=['users'],
  )
