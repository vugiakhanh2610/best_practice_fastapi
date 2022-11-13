from models.app_user import AppUser
from schemas.app_user_schema import AppUserCreate, AppUserResponse, AppUserUpdate
from services.base_service import CRUDBaseService


class AppUserService(CRUDBaseService[AppUserCreate, AppUserUpdate, AppUserResponse]):
  # def create(self, session: Session, payload: AppUserCreate):
  ...
  
app_user_service = AppUserService(AppUser)
