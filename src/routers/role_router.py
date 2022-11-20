import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.listing_schema import ListingParams
from schemas.role_schema import RoleCreate, RoleResponse, RoleResponsePage, RoleUpdate
from services.role_service import role_service

router = APIRouter(tags=['roles'])
RESOURCE = '/roles'

@cbv(router)
class AppUserRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def create(self, payload: RoleCreate):
    role = role_service.create(self.session, payload)
    self.session.commit()
    self.session.refresh(role)
    return APIResponse[RoleResponse](data=jsonable_encoder(role))
  
  @router.get(RESOURCE + '/{id}')
  def get_by_id(self, id: uuid.UUID):
    data = role_service.get_by_id(self.session, id)
    return APIResponse[RoleResponse](data=jsonable_encoder(data))
  
  @router.put(RESOURCE + '/{id}')
  def update_by_id(self, id: uuid.UUID, payload: RoleUpdate):
    role_service.update_by_id(self.session, id, payload)
    self.session.commit()
    return APIResponse()
    
  @router.get(RESOURCE)
  def get_list(
    self,
    params: ListingParams = Depends(),
    keyword: str = None
  ):
    query = role_service.get_query(self.session, keyword)
    data = role_service.get_list(query, params)
    return APIResponse[PaginatedData[RoleResponsePage]](data=data)
  
  @router.delete(RESOURCE + '/{id}')
  def delete_by_id(self, id: uuid.UUID):
    role_service.delete_by_id(self.session, id)
    self.session.commit()
    return APIResponse()
