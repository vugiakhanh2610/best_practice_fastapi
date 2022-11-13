import os
import sys

sys.path.append(f'{os.getcwd()}/src')
from main import create_tables, drop_tables

if __name__ == '__main__':
  drop_tables()
  create_tables()
