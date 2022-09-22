from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Time
from sqlalchemy.sql import func

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True) # Auto-increment should be default
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  disabled = Column(Boolean)
  entry_date = Column(Time, server_default=func.now())
  modified_date = Column(Time, onupdate=func.now())
  
  def __init__(self, username, password, disabled):
    self.username = username
    self.password = password
    self.disabled = disabled