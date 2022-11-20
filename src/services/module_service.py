from models.module import Module
from schemas.module_schema import ModuleCreate, ModuleUpdate
from services.base_service import CRUDBaseService


class ModuleService(CRUDBaseService[ModuleCreate, ModuleUpdate, Module]):
  ...
  
module_service = ModuleService(Module)
