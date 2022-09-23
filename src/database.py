from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from setting import Setting

engine = create_engine(url=Setting().DB_CONNECTION_STR, echo=False) # echo = show-sql
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# inherit from this class to create each of the database models 
Base = declarative_base()
# class Base:
#   id: Any
#   __name__: str
#   # generate tablename from classname
#   @declared_attr
#   def __tablename__(cls) -> str:
#     return cls.__name__.lower()

# create a database session for each request - close it after finishing the request
def get_session() -> Generator:
  try:
    session = Session()
    yield session
  finally:
    session.close()
    
