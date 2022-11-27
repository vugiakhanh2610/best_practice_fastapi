from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from database import Base


class Group(Base):
  __tablename__ = 'group'
  id = Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True)
  name = Column(String(255))
  app_users = relationship('AppUser', back_populates='group')
  module_permissions = relationship('ModulePermission', backref='group', cascade='all, delete-orphan')

  created_by = Column(String, nullable=False)
  created_time = Column(DateTime(timezone=True), nullable=False)
  updated_by = Column(String)
  updated_time = Column(DateTime(timezone=True))
