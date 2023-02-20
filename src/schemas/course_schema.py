from typing import Optional

from pydantic import BaseModel


class CourseCreate(BaseModel):
  image: Optional[str]
  title: Optional[str]
  author: Optional[str]
  rating: Optional[int]
  price: Optional[int]
  bestSeller: Optional[bool]
  buyAmount: Optional[int]

class CourseUpdate(CourseCreate):
  ...
