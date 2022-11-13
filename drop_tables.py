import os
import sys

sys.path.append(f'{os.getcwd()}/src')
from database import Base, engine


def drop_tables():
  Base.metadata.drop_all(bind=engine, checkfirst=True)
