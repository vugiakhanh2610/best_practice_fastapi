from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.user import User
from schemas.user_schema import UserCreate, UserResponse
from utils.hashing_util import Hasher


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
    return 'Deleted successfully'
  
  # def login(session: Session, payload: UserLogin):
  #   user: User = session.query(User).filter(User.email == payload.email).first()
  #   if not user:
  #     raise HTTPException(status_code=404, detail='User not exist')
  #   if not Hasher.verify_hashed_str(payload.password, user.password):
  #     raise HTTPException(status_code=401, detail='Invalid password')
    
  #   access_token = generate_token(user.email)
  #   return {'access_token': access_token}
