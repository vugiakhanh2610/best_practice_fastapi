from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, Table

from database import Base

app_user_role = Table(
  'app_user_role',
  Base,
  Column('app_user.id', GUID, primary_key=True),
  Column('role.id', GUID, primary_key=True)
)
