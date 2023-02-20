
from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.course_schema import CourseCreate, CourseUpdate
from services.course_service import course_service

RESOURCE = 'courses'
router = APIRouter(tags=[RESOURCE])

@cbv(router)
class AppUserRouter:
  
  #: UserSession = Depends(get)
  session: Session = Depends(get_session)
  
  @router.post(f'/{RESOURCE}')
  def create(self, request: Request, payload: CourseCreate):
    course = course_service.create(self.session, payload)
    self.session.commit()
    self.session.refresh(course)
    return course
  
  @router.get(f'/{RESOURCE}' + '/{id}')
  def get_by_id(self, request: Request, id: int):
    return course_service.get_by_id(self.session, id)
  
  @router.put(f'/{RESOURCE}' + '/{id}')
  def update(self, request: Request, id: int, payload: CourseUpdate):
    course = course_service.update_by_id(self.session, id, payload)
    self.session.commit()
    self.session.refresh(course)
    return course
  
  @router.delete(f'/{RESOURCE}' + '/{id}')
  def delete_by_id(self, request: Request, id: int):
    course_service.delete_by_id(self.session, id)
    self.session.commit()
    return

  @router.get(f'/{RESOURCE}')
  def get_list(self):
    return course_service.get_all(self.session)
