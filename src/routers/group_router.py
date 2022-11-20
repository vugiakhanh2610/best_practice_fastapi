import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.group_schema import GroupCreate, GroupResponse, GroupResponsePage, GroupUpdate
from schemas.listing_schema import ListingParams
from security import get_current_user
from services.group_service import group_service

router = APIRouter(tags=['groups'])
RESOURCE = '/groups'

@cbv(router)
class GroupRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def create(self, request: Request, payload: GroupCreate, current_user = Depends(get_current_user)):
    group_service.create(self.session, payload)
    self.session.commit()
    return APIResponse()
    
  @router.get(RESOURCE + '/{id}')
  def get_by_id(self, request: Request, id: uuid.UUID, current_user = Depends(get_current_user)):
    data = group_service.get_by_id(self.session, id)
    return APIResponse[GroupResponse](data=jsonable_encoder(data))
  
  @router.put(RESOURCE + '/{id}')
  def update_by_id(self, request: Request, id: uuid.UUID, payload: GroupUpdate, current_user = Depends(get_current_user)):
    group_service.update_by_id(self.session, id, payload)
    self.session.commit()
    return APIResponse()
  
  @router.delete(RESOURCE + '/{id}')
  def delete_by_id(self, request: Request, id: uuid.UUID, current_user = Depends(get_current_user)):
    group_service.delete_by_id(self.session, id)
    self.session.commit()
    return APIResponse()
  
  @router.get(RESOURCE)
  def get_list(
    self,
    request: Request,
    params: ListingParams = Depends(),
    keyword: str = None,
    current_user = Depends(get_current_user)
  ):
    query = group_service.get_query(self.session, keyword)
    data = group_service.get_list(query, params)
    return APIResponse[PaginatedData[GroupResponsePage]](data=data)
