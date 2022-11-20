from models.module_permission import ModulePermission
from schemas.module_permission_schema import ModulePermissionCreate, ModulePermissionUpdate
from services.base_service import CRUDBaseService


class ModulePermissionService(CRUDBaseService[ModulePermissionCreate, ModulePermissionUpdate, ModulePermission]):
  ...
  
ModulePermission_service = ModulePermissionService(ModulePermission)
