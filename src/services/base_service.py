import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base
from utils.helper_utils import set_value

SchemaCreateType = TypeVar('SchemaCreateType', bound=BaseModel)
SchemaUpdateType = TypeVar('SchemaUpdateType', bound=BaseModel)
SchemaResponseType = TypeVar('SchemaResponseType', bound=BaseModel)
ModelType = TypeVar('ModelType', bound=Base)


class CRUDBaseService(Generic[SchemaCreateType, SchemaUpdateType, SchemaResponseType]):
  
  def __init__(self, Model: ModelType) -> None:
    self.Model = Model
  
  def create(self, session: Session, payload: SchemaCreateType):
    model = self.Model()
    set_value(model, payload)
    session.add(model)
    return

  def get_by_id(self, session: Session, id: uuid.UUID) -> ModelType:
    return session.query(self.Model).filter(self.Model.id == id).one()

  def update_by_id(self, session: Session, id: uuid.UUID, payload: SchemaUpdateType):
    model = self.get_by_id(session, id)
    set_value(model, payload)
    return 

  def delete_by_id(self, session: Session, id: uuid.UUID):
    model = self.get_by_id(session, id)
    session.delete(model)
    return
