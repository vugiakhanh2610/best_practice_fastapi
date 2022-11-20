import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

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

class AppUserResponse(AppUserCreate):
  id: uuid.UUID
  group: GroupResponse

class AppUserResponsePage(BaseModel):
  id: uuid.UUID
  email: EmailStr
  username: str
