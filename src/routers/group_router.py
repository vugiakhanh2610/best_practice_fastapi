import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv

from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.group_schema import GroupCreate, GroupResponse, GroupResponsePage, GroupUpdate
from schemas.listing_schema import ListingParams
from security import UserSession, auth_check, get_current_user
from services.group_service import group_service

RESOURCE = 'groups'
router = APIRouter(tags=[RESOURCE])

@cbv(router)
class GroupRouter:
  
  current_user: UserSession = Depends(get_current_user)
  
  @router.post(f'/{RESOURCE}')
  @auth_check([RESOURCE])
  def create(self, request: Request, payload: GroupCreate):
    group_service.create(self.current_user.session, payload)
    self.current_user.session.commit()
    return APIResponse()
    
  @router.get(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def get_by_id(self, request: Request, id: uuid.UUID):
    data = group_service.get_by_id_with_module_permission(self.current_user.session, id)
    return APIResponse[GroupResponse](data=jsonable_encoder(data))
  
  @router.put(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def update_by_id(self, request: Request, id: uuid.UUID, payload: GroupUpdate):
    group_service.update_by_id(self.current_user.session, id, payload)
    self.current_user.session.commit()
    return APIResponse()
  
  @router.delete(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def delete_by_id(self, request: Request, id: uuid.UUID):
    group_service.delete_by_id(self.current_user.session, id)
    self.current_user.session.commit()
    return APIResponse()
  
  @router.get(f'/{RESOURCE}')
  @auth_check([RESOURCE])
  def get_list(
    self,
    request: Request,
    params: ListingParams = Depends(),
    keyword: str = None,
  ):
    query = group_service.get_query(self.current_user.session, keyword)
    data = group_service.get_list(query, params)
    return APIResponse[PaginatedData[GroupResponsePage]](data=data)
