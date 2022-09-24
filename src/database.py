import fnmatch
import os
from typing import Generator

import databases
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from setting import Setting

engine = create_engine(url=Setting().DB_CONNECTION_STR, echo=False) # echo = show-sql

# Difference between flush and commit: https://www.youtube.com/watch?v=1atze8xe9wg&ab_channel=HowtoFixYourComputer
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

def get_number_models() -> int:
  path_to_models_dir = f'{os.getcwd()}/src/models'
  return len(fnmatch.filter(os.listdir(path_to_models_dir), '*.py'))
   
async def check_db_info():
  try:
    db = databases.Database(Setting().DB_CONNECTION_STR)
    if not db.is_connected:
      await db.connect()
      db_version = await db.execute('SELECT version()')
      number_tables = await db.execute(f"select count(*) from information_schema.tables where table_schema = 'public'")
      number_models = get_number_models()
      
      logger.info(db_version)
      logger.info(f'Number of tables in database: {number_tables}')
      logger.info(f'Number of models: {number_models}')
      
      if int(number_tables) != number_models:
        raise RuntimeError('Incorrect number of tables in database')
  except Exception as e:
    raise e
    
