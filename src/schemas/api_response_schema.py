from http import HTTPStatus
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataType = TypeVar('DataType', bound=BaseModel)

class APIResponse(GenericModel, Generic[DataType]):
  error_details: str = None
  message: str = HTTPStatus(200).phrase
  data: Optional[DataType]

class PaginatedData(GenericModel, Generic[DataType]):
  total_items: int
  total_pages: int
  items: list[DataType]
