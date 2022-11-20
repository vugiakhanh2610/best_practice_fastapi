import uuid
from typing import Optional

from pydantic import BaseModel


class ModulePermissionCreate(BaseModel):
  group_id: uuid.UUID
  module_id: uuid.UUID
  read: bool
  create: bool
  update: bool
  delete: bool

class ModulePermissionUpdate(BaseModel):
  read: Optional[bool]
  create: Optional[bool]
  update: Optional[bool]
  delete: Optional[bool]

class ModulePermissionResponse(ModulePermissionCreate):
  id: uuid.UUID
