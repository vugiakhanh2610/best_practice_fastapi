import uuid

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from database import get_session
from schemas.api_response_schema import APIResponse, PaginatedData
from schemas.listing_schema import ListingParams
from schemas.module_schema import ModuleCreate, ModuleResponse, ModuleResponsePage, ModuleUpdate
from security import get_current_user
from services.module_service import module_service

router = APIRouter(tags=['modules'])
RESOURCE = '/modules'

@cbv(router)
class ModuleRouter:
  
  session: Session = Depends(get_session)
  
  @router.post(RESOURCE)
  def create(self, request: Request, payload: ModuleCreate, current_user = Depends(get_current_user)):
    module = module_service.create(self.session, payload)
    self.session.commit()
    self.session.refresh(module)
    return APIResponse[ModuleResponse](data=jsonable_encoder(module))
    
  @router.get(RESOURCE + '/{id}')
  def get_by_id(self, request: Request, id: uuid.UUID, current_user = Depends(get_current_user)):
    data = module_service.get_by_id(self.session, id)
    return APIResponse[ModuleResponse](data=jsonable_encoder(data))
  
  @router.put(RESOURCE + '/{id}')
  def update_by_id(self, request: Request, id: uuid.UUID, payload: ModuleUpdate, current_user = Depends(get_current_user)):
    module_service.update_by_id(self.session, id, payload)
    self.session.commit()
    return APIResponse()
  
  @router.delete(RESOURCE + '/{id}')
  def delete_by_id(self, request: Request, id: uuid.UUID, current_user = Depends(get_current_user)):
    module_service.delete_by_id(self.session, id)
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
    query = module_service.get_query(self.session, keyword)
    data = module_service.get_list(query, params)
    return APIResponse[PaginatedData[ModuleResponsePage]](data=data)
