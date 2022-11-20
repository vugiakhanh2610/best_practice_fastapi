import uuid

from pydantic import BaseModel


class GroupCreate(BaseModel):
  name: str

class GroupUpdate(GroupCreate):
  ...

class GroupResponse(GroupCreate):
  id: uuid.UUID
  
class GroupResponsePage(GroupResponse):
  ...
