from sqlalchemy.orm import Session

from models.course import Course
from schemas.course_schema import CourseCreate, CourseUpdate
from services.base_service import CRUDBaseService


class CourseSerivice(CRUDBaseService[CourseCreate, CourseUpdate]):
  
  def get_all(self, session: Session):
    return session.query(Course).all()
  
course_service = CourseSerivice(Course)
