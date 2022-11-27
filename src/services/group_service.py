import uuid

from sqlalchemy.orm import Session, joinedload

from models.group import Group
from models.module_permission import ModulePermission
from schemas.group_schema import GroupCreate, GroupUpdate
from services.base_service import CRUDBaseService
from services.module_permission_service import module_permission_service
from utils.helper_utils import set_value


class GroupService(CRUDBaseService[GroupCreate, GroupUpdate]):
  def create(self, session: Session, payload: GroupCreate):
    group = Group()
    set_value(group, payload, {'module_permissions'})
    session.add(group)
    session.flush()
    for data in payload.module_permissions:
      module_permission = module_permission_service.create(session, group.id, data)
      group.module_permissions.append(module_permission)

    return group
  
  def get_by_id_with_module_permission(self, session: Session, id: uuid.UUID) -> Group:
    return session.query(Group).options(joinedload(Group.module_permissions).joinedload(ModulePermission.module)).filter(Group.id == id).one()
  
  def update_by_id(self, session: Session, id: uuid.UUID, payload: GroupUpdate):
    group = self.get_by_id(session, id)
    set_value(group, payload, {'module_permissions'})
    
    list_before_updated: list = group.module_permissions.copy()
    if payload.module_permissions:
      for data in payload.module_permissions:
        module_permission = module_permission_service.get_by_id(session, id, data.module_id)
        if module_permission:
          set_value(module_permission, data, {'module_id'})
          list_before_updated.remove(module_permission)
        else:
          module_permission_service.create(session, id, data)
      for module_permission in list_before_updated:
        session.delete(module_permission)
        
  def get_query(self, session: Session, keyword: str):
    condition = []
    # Search
    if keyword:
      condition.append(
        Group.name.ilike(f'%{keyword}%')
      )
    return super().get_query(session, condition)

group_service = GroupService(Group)
