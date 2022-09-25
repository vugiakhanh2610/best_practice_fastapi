from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
  # id: Optional[int] = None
  username: Optional[str] = None
  email: Optional[EmailStr] = None
  password: Optional[str] = None
  disabled: Optional[bool] = None
  
  # https://pydantic-docs.helpmanual.io/usage/model_config/
  class Config:
    anystr_strip_whitespace = True
    extra = 'forbid'
    orm_mode = True # https://pydantic-docs.helpmanual.io/usage/models/#orm-mode-aka-arbitrary-class-instances

class UserResponse(BaseModel):
  username: str
  email: EmailStr
  disabled: Optional[bool]

class UserCreate(UserBase):
  username: str = Field(max_length=50)
  email: EmailStr
  password: str 

class UserLogin(BaseModel):
  email: str
  password: str
  
