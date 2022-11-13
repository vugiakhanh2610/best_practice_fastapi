from typing import Optional

from pydantic import BaseModel


class RoleCreate(BaseModel):
  name: str
  
class RoleUpdate(RoleCreate):
  name: Optional[str]

class RoleResponse(RoleCreate):
  ...
