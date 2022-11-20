from sqlalchemy.orm import Session

from models.module import Module
from schemas.module_schema import ModuleCreate, ModuleUpdate
from services.base_service import CRUDBaseService


class ModuleService(CRUDBaseService[ModuleCreate, ModuleUpdate]):
  
  def get_query(self, session: Session, keyword: str):
    condition = []
    # Search
    if keyword:
      condition.append(Module.name.ilike(f'%{keyword}%'))
    return super().get_query(session, condition)
  
module_service = ModuleService(Module)
