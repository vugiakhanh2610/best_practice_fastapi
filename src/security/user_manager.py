from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from loguru import logger

from database import get_async_session
from models.user import User
from setting import settings


async def get_user_db(session = Depends(get_async_session)):
  yield SQLAlchemyUserDatabase(session, User)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
  reset_password_token_secret = settings.JWT_SECRET_KEY
  verification_token_secret = settings.JWT_SECRET_KEY
  
  reset_password_token_lifetime_seconds = settings.TOKEN_EXPIRY_IN_MINUTES
  verification_token_lifetime_seconds = settings.TOKEN_EXPIRY_IN_MINUTES
  async def on_after_register(self, user: User, request: Optional[Request] = None):
    logger.info(f'User {user.email} has registered.')
    
  async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
    logger.info(f'User {user.email} has forgot their password. Reset token: {token}')
    
  async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
    logger.info(f'Verification requested for user {user.email}. Verification token: {token}')

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
  yield UserManager(user_db)
  
