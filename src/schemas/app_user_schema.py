import uuid
from typing import Optional

from pydantic import BaseModel

from schemas.role_schema import RoleResponse


class AppUserCreate(BaseModel):
  username: str
  email: str
  roles: list[uuid.UUID]
  
class AppUserUpdate(BaseModel):
  username: Optional[str]
  roles: list[uuid.UUID]

class AppUserPassword(BaseModel):
  password: str

class AppUserResponse(BaseModel):
  username: str
  email: str
  roles: RoleResponse
