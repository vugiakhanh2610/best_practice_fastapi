from typing import Literal, Optional

from pydantic import BaseModel, conint


class ListingParams(BaseModel):
  page_index: Optional[conint(ge=0)] = 0
  page_size: Optional[conint(gt=0)] = 10
  sort_by: Optional[str] = 'created_time'
  order: Literal['asc', 'desc'] = 'desc'
