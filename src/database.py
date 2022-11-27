import contextlib
import fnmatch
import os
import warnings
from typing import Generator

import databases
from fastapi import HTTPException
from loguru import logger
from sqlalchemy import MetaData, create_engine, schema
from sqlalchemy.exc import NoResultFound, SAWarning
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists

from setting import settings

db_connection_url = f'postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

engine = create_engine(
  url=db_connection_url,
  echo=False,
  connect_args={
    'options': f'-csearch_path={settings.DB_SCHEMA}',
    'options': '-c timezone=utc',
  }
)

# Difference between flush and commit: https://www.youtube.com/watch?v=1atze8xe9wg&ab_channel=HowtoFixYourComputer
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

# inherit from this class to create each of the database models 
Base = declarative_base(metadata=MetaData(schema=f'{settings.DB_SCHEMA}'))
# class Base:
#   id: Any
#   __name__: str
#   # generate tablename from classname
#   @declared_attr
#   def __tablename__(cls) -> str:
#     return cls.__name__.lower()

def create_db():
  logger.debug('Creating Database')
  if not database_exists(db_connection_url):
    create_database(db_connection_url)

def create_schema():
  logger.debug('Creating Schema')
  if not engine.dialect.has_schema(engine, f'{settings.DB_SCHEMA}'):
    engine.execute(schema.CreateSchema(f'{settings.DB_SCHEMA}'))

def create_tables():
  logger.debug('Creating Tables')
  Base.metadata.create_all(bind=engine, checkfirst=True)

def drop_tables():
  logger.debug('Dropping Tables')
  Base.metadata.drop_all(bind=engine, checkfirst=True)

# For foreign key problem in future, refer to this solution https://gist.github.com/absent1706/3ccc1722ea3ca23a5cf54821dbc813fb
def truncate_db():
  logger.debug('Truncating Tables')
  tables = Base.metadata.sorted_tables
  
  # calls the connection.close() method when when a block of code is entered and exited
  with contextlib.closing(engine.connect()) as ctx:
    transaction = ctx.begin()
    ctx.execute('TRUNCATE TABLE {} RESTART IDENTITY CASCADE'.format(','.join(table.name for table in tables)))
    transaction.commit()

# create a database session for each request - close it after finishing the request
def get_session() -> Generator:
  try:
    with warnings.catch_warnings():
      warnings.simplefilter('ignore', category=SAWarning)
      session = Session()
      yield session
  except NoResultFound as e:
    raise HTTPException(status_code=404, detail=e._message())
  finally:
    logger.debug('Closing sesssion')
    session.close()

def get_number_models() -> int:
  path_to_models_dir = f'{os.getcwd()}/src/models'
  return len(fnmatch.filter(os.listdir(path_to_models_dir), '*.py')) - 1 # Not count file __init__.py
   
async def check_db_info():
  try:
    db = databases.Database(db_connection_url)
    if not db.is_connected:
      await db.connect()
      db_version = await db.execute('SELECT version()')
      number_tables = await db.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{settings.DB_SCHEMA}'")
      number_models = get_number_models()
      
      logger.info(db_version)
      logger.info(f'Number of tables in database: {number_tables}')
      logger.info(f'Number of models: {number_models}')
      
      if int(number_tables) != number_models:
        logger.warning('Incorrect number of tables in database')
        drop_tables()
        create_tables()
        logger.info(f'Number of tables in database: {number_tables}')
        
  except Exception as e:
    raise e
    
