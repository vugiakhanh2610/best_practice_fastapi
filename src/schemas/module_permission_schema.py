import uuid
from typing import Optional

from pydantic import BaseModel

from schemas.module_schema import ModuleResponse


class ModulePermissionCreate(BaseModel):
  module_id: uuid.UUID
  read: bool
  create: bool
  update: bool
  delete: bool

class ModulePermissionUpdate(ModulePermissionCreate):
  read: Optional[bool]
  create: Optional[bool]
  update: Optional[bool]
  delete: Optional[bool]

class ModulePermissionResponse(BaseModel):
  read: bool
  create: bool
  update: bool
  delete: bool
  module: ModuleResponse
