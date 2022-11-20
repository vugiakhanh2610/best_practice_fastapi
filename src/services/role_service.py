from sqlalchemy.orm import Session

from models.role import Role
from schemas.role_schema import RoleCreate, RoleResponse, RoleUpdate
from services.base_service import CRUDBaseService


class RoleService(CRUDBaseService[RoleCreate, RoleUpdate, RoleResponse]):
  
  def get_query(self, session: Session, keyword: str):
    condition = []
    # Search
    if keyword:
      condition.append(Role.name.ilike(f'%{keyword}%'))
    
    return super().get_query(session, condition)
  
role_service = RoleService(Role)
