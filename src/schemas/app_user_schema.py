import uuid
from typing import Optional

from pydantic import BaseModel

from schemas.role_schema import RoleResponse


class AppUserCreate(BaseModel):
  username: str
  email: str
  
class AppUserUpdate(BaseModel):
  username: Optional[str]
  password: str
  roles: list[uuid.UUID]

class AppUserResponse(BaseModel):
  username: str
  email: str
  roles: RoleResponse
