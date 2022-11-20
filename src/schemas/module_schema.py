import uuid

from pydantic import BaseModel


class ModuleCreate(BaseModel):
  name: str

class ModuleUpdate(ModuleCreate):
  ...

class ModuleResponse(ModuleCreate):
  id: uuid.UUID
  
class ModuleResponsePage(ModuleResponse):
  ...
