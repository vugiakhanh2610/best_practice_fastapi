from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, String)
from sqlalchemy.orm import relationship

from database import Base


class AppUser(Base):
  __tablename__ = 'app_user'
  id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  username = Column(String(255), nullable=False)
  email = Column(String(255), nullable=False)
  password = Column(String(255))
  is_verified = Column(Boolean, nullable=False)
  verify_token = Column(String, unique=True)
  group_id = Column(GUID, ForeignKey('group.id', ondelete='SET NULL'))
  group = relationship('Group', back_populates='app_users')

  created_by = Column(String, nullable=False)
  created_time = Column(DateTime(timezone=True), nullable=False)
  updated_by = Column(String)
  updated_time = Column(DateTime(timezone=True))
