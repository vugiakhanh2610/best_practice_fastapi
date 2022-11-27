import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator

from schemas.group_schema import GroupResponse


class AppUserCreate(BaseModel):
  username: str
  email: EmailStr
  group_id: uuid.UUID
  
class AppUserUpdate(BaseModel):
  username: Optional[str]
  group_id: Optional[uuid.UUID]

class AppUserPassword(BaseModel):
  password: str
  confirm_password: str
  
  @validator('confirm_password')
  def match_password(cls, v, values):
    if 'password' in values and v != values['password']:
      raise HTTPException(status_code=422, detail='Confirm password does not match')

class AppUserResponse(AppUserCreate):
  id: uuid.UUID
  group: GroupResponse

class AppUserResponsePage(BaseModel):
  id: uuid.UUID
  email: EmailStr
  username: str

class AppUserToken(BaseModel):
  token: str
