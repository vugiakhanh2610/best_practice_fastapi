from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Course(Base):
  __tablename__ = 'course'
  id = Column(Integer, primary_key=True)
  image = Column(String(255))
  title = Column(String(255))
  author = Column(String(255))
  rating = Column(Integer)
  price = Column(Integer)
  bestSeller = Column(Boolean)
  buyAmount = Column(Integer)
