from fastapi_utils.guid_type import GUID
from sqlalchemy import Boolean, Column, ForeignKey, Table

from database import Base

ModulePermission = Table(
  'module_permission',
  Base.metadata,
  Column('group_id', GUID, ForeignKey('group.id'), primary_key=True),
  Column('module_id', GUID, ForeignKey('module.id'), primary_key=True),
  Column('read', Boolean, nullable=False),
  Column('create', Boolean, nullable=False),
  Column('update', Boolean, nullable=False),
  Column('delete', Boolean, nullable=False)
)
