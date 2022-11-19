from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from database import Base
from models.app_user_role import app_user_role


class AppUser(Base):
  __tablename__ = 'app_user'
  id = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL)
  username = Column(String(255), nullable=False)
  email = Column(String(255), nullable=False)
  password = Column(String(255))
  is_verified = Column(Boolean, nullable=False)
  verify_token = Column(String, unique=True)
  roles = relationship('Role', secondary=app_user_role, back_populates='app_users')
