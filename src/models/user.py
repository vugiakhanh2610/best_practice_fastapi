from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String

from database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
  __tablename__ = 'users'
  username = Column(String, nullable=False)
