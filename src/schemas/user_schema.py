import uuid
from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import Field


class UserResponse(BaseUser[uuid.UUID]):
  username: Optional[str] = Field(max_length=50)
  
  # https://pydantic-docs.helpmanual.io/usage/model_config/
  # class Config:
  #   anystr_strip_whitespace = True
  #   extra = 'forbid'
  #   orm_mode = True # https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances

class UserCreate(BaseUserCreate):
  username: str = Field(max_length=50)
  
class UserUpdate(BaseUserUpdate):
  username: Optional[str] = Field(max_length=50)

  
