from http import HTTPStatus
from typing import Any, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, validator


class APIResponseBase(BaseModel):
  error_details: Optional[str]
  message: str
  data: Optional[Any]
  
class APIResponseSuccess(APIResponseBase):
  message: str = HTTPStatus(200).phrase
  
  @validator('data')
  def serialize_to_json(cls, v, values):
    return jsonable_encoder(v)

class APIResponseError(APIResponseBase):
  error_details: str
  message: str = 'ERROR'
