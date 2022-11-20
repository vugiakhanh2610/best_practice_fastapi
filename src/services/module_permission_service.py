import uuid

from sqlalchemy.orm import Session

from models.module_permission import ModulePermission
from schemas.module_permission_schema import ModulePermissionCreate, ModulePermissionUpdate
from services.base_service import CRUDBaseService


class ModulePermissionService(CRUDBaseService[ModulePermissionCreate, ModulePermissionUpdate]):
  
  def create(self, session: Session, group_id: uuid.UUID, payload: ModulePermissionCreate):
    module_permission = ModulePermission(**payload.dict())
    module_permission.group_id = group_id
    session.add(module_permission)
    return module_permission
  
  def get_by_id(self, session: Session, group_id: uuid.UUID, module_id: uuid.UUID) -> ModulePermission:
    return session.query(ModulePermission).filter(ModulePermission.group_id == group_id, ModulePermission.module_id == module_id).first()
  
module_permission_service = ModulePermissionService(ModulePermission)
