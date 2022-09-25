from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  
# class User(SQLAlchemyBaseUserTableUUID, Base):
#   __tablename__ = 'users'

  # id = Column(Integer, primary_key=True) # Auto-increment should be default
  # username = Column(String, nullable=False)
  # email = Column(String, nullable=False)
  # password = Column(String, nullable=False)
  # disabled = Column(Boolean)
  # entry_date = Column(Time, server_default=func.now())
  # modified_date = Column(Time, onupdate=func.now())
  
  # def __init__(self, username, email, password, disabled):
  #   self.username = username
  #   self.email = email
  #   self.password = password
  #   self.disabled = disabled
