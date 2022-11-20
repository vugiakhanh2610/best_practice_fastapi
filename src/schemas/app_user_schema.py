import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class AppUserCreate(BaseModel):
  username: str
  email: EmailStr
  group_id: uuid.UUID
  
class AppUserUpdate(BaseModel):
  username: Optional[str]
  # group: 

class AppUserPassword(BaseModel):
  password: str

class AppUserResponse(AppUserCreate):
  id: uuid.UUID
  # group: list[RoleResponse]

class AppUserResponsePage(BaseModel):
  id: uuid.UUID
  email: EmailStr
  username: str
