import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv

from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.listing_schema import ListingParams
from schemas.module_schema import ModuleCreate, ModuleResponse, ModuleResponsePage, ModuleUpdate
from security import UserSession, auth_check, get_current_user
from services.module_service import module_service

RESOURCE = 'modules'
router = APIRouter(tags=[RESOURCE])

@cbv(router)
class ModuleRouter:
  
  current_user: UserSession = Depends(get_current_user)
  
  @router.post(f'/{RESOURCE}')
  # @auth_check([RESOURCE])
  def create(self, request: Request, payload: ModuleCreate):
    module = module_service.create(self.current_user.session, payload)
    self.current_user.session.commit()
    self.current_user.session.refresh(module)
    return APIResponse[ModuleResponse](data=jsonable_encoder(module))
    
  @router.get(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def get_by_id(self, request: Request, id: uuid.UUID):
    data = module_service.get_by_id(self.current_user.session, id)
    return APIResponse[ModuleResponse](data=jsonable_encoder(data))
  
  @router.put(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def update_by_id(self, request: Request, id: uuid.UUID, payload: ModuleUpdate):
    module_service.update_by_id(self.current_user.session, id, payload)
    self.current_user.session.commit()
    return APIResponse()
  
  @router.delete(f'/{RESOURCE}' + '/{id}')
  @auth_check([RESOURCE])
  def delete_by_id(self, request: Request, id: uuid.UUID):
    module_service.delete_by_id(self.current_user.session, id)
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
    query = module_service.get_query(self.current_user.session, keyword)
    data = module_service.get_list(query, params)
    return APIResponse[PaginatedData[ModuleResponsePage]](data=data)
