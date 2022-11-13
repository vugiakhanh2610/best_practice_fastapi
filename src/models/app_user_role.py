from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, ForeignKey, Table

from database import Base

app_user_role= Table(
  'app_user_role',
  Base.metadata,
  Column('app_user_id', GUID, ForeignKey('app_user.id'), primary_key=True),
  Column('role_id', GUID, ForeignKey('role.id'), primary_key=True)
)
