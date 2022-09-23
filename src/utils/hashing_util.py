from passlib.context import CryptContext

ctx = CryptContext(schemes=['bcrypt'])

class Hasher:
  
  def hash_obj(obj: object) -> str:
    return ctx.hash(obj)
  
  def verify_hashed_str(obj: object, hashed_obj: str) -> bool:
    return ctx.verify(obj, hashed_obj)
