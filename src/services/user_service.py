from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate

class UserService: 
  
  def get_all(session: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return session.query(User).offset(skip).limit(limit).all()
  
  def get_by_id(session: Session, id: int) -> User:
    return session.query(User).filter(User.id == id).first()
  
  def create(session: Session, payload: UserCreate) -> int:
    user = User(**payload.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user.id
  
  def update(session: Session, id: int, payload: UserCreate) -> int:
    user = session.query(User).filter(User.id == id).first()
    if not user:
      raise HTTPException(status_code=404, detail="Not found")
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
  