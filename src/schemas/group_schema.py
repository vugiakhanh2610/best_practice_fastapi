import uuid
from typing import Optional

from pydantic import BaseModel

from schemas.module_permission_schema import ModulePermissionCreate, ModulePermissionResponse, ModulePermissionUpdate


class GroupCreate(BaseModel):
  name: str
  module_permissions: list[ModulePermissionCreate]

class GroupUpdate(GroupCreate):
  name: Optional[str]
  module_permissions: Optional[list[ModulePermissionUpdate]]

class GroupResponse(GroupCreate):
  id: uuid.UUID
  module_permissions: list[ModulePermissionResponse]
  
class GroupResponsePage(BaseModel):
  id: uuid.UUID
  name: str
