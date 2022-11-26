import os
import sys

sys.path.append(f'{os.getcwd()}/src')
from sqlalchemy.schema import DropTable
from sqlalchemy.sql import table

from database import Session
from setting import settings


def run_alembic():
  session = Session()
  session.execute(DropTable(table('alembic_version', schema=settings.DB_SCHEMA), if_exists=True))
  session.commit()
  session.close()
  os.system('sh bin/migrate.sh')

if __name__ == '__main__':
  run_alembic()
