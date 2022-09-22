from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from utils.hashing_util import Hasher
from models.user import User
from schemas.user_schema import UserCreate, UserResponse

class UserService: 
  
  def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[UserResponse]:
    return jsonable_encoder(session.query(User).offset(skip).limit(limit).all())
  
  def get_by_id(session: Session, id: int) -> UserResponse:
    user = session.query(User).filter(User.id == id).first()
    if not user:
      raise HTTPException(status_code=404, detail=f'User with id {id} not found')
    return jsonable_encoder(user)
  
  def create(session: Session, payload: UserCreate) -> int:
    user = User(**payload.dict())
    user.password = Hasher.hash_obj(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.id
  
  def update(session: Session, id: int, payload: UserCreate) -> int:
    user = session.query(User).filter(User.id == id).first()
    if not user:
      raise HTTPException(status_code=404, detail=f'User with id {id} not found')
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
      if hasattr(user, key):
        setattr(user, key, value)
    session.commit()
    return user.id
  
  def delete_by_id(session: Session, id: int):
    session.query(User).filter(User.id == id).delete()
    session.commit()
    return "Deleted successfully"
  