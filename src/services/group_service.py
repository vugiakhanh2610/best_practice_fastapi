from models.group import Group
from schemas.group_schema import GroupCreate, GroupUpdate
from services.base_service import CRUDBaseService


class GroupService(CRUDBaseService[GroupCreate, GroupUpdate, Group]):
  ...
  
group_service = GroupService(Group)
