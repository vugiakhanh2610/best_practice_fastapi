from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, DateTime, String

from database import Base


class Module(Base):
  __tablename__ = 'module'
  id = Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True)
  name = Column(String(255))

  created_by = Column(String, nullable=False)
  created_time = Column(DateTime(timezone=True), nullable=False)
  updated_by = Column(String)
  updated_time = Column(DateTime(timezone=True))
