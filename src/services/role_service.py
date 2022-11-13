from models.role import Role
from schemas.role_schema import RoleCreate, RoleResponse, RoleUpdate
from services.base_service import CRUDBaseService


class RoleService(CRUDBaseService[RoleCreate, RoleUpdate, RoleResponse]):
  pass
  
role_service = RoleService(Role)
