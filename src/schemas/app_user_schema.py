import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from schemas.role_schema import RoleResponse


class AppUserCreate(BaseModel):
  username: str
  email: EmailStr
  roles: list[uuid.UUID]
  
class AppUserUpdate(BaseModel):
  username: Optional[str]
  roles: list[uuid.UUID]

class AppUserPassword(BaseModel):
  password: str

class AppUserResponse(AppUserCreate):
  id: uuid.UUID
  roles: list[RoleResponse]

class AppUserResponsePage(BaseModel):
  id: uuid.UUID
  email: EmailStr
  username: str
