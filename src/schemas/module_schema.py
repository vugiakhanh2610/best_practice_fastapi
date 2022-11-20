import uuid
from typing import Optional

from pydantic import BaseModel


class ModuleCreate(BaseModel):
  name: str

class ModuleUpdate(ModuleCreate):
  name: Optional[str]

class ModuleResponse(ModuleCreate):
  id: uuid.UUID
  
class ModuleResponsePage(ModuleResponse):
  ...
