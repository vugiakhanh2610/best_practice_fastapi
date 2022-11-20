from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base
from models.module_permission import ModulePermission


class Module(Base):
  __tablename__ = 'module'
  id = Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True)
  name = Column(String(255))
  groups = relationship('Group', secondary=ModulePermission, back_populates='modules')
