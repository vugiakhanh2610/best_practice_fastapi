from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database import Base
from models.app_user_role import app_user_role


class Role(Base):
  __tablename__ = 'role'
  id = Column(GUID, server_default=GUID_SERVER_DEFAULT_POSTGRESQL, primary_key=True)
  name = Column(String(255))
  users = relationship('AppUser', secondary=app_user_role)
