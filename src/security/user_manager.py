from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from loguru import logger

from database import get_async_session
from models.user import User


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
  
