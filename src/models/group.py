from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base
from models.module_permission import ModulePermission


class Group(Base):
  __tablename__ = 'group'
  id = Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True)
  name = Column(String(255))
  app_users = relationship('AppUser', back_populates='group')
  modules = relationship('Module', secondary=ModulePermission, back_populates='groups')
