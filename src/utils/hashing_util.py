from passlib.context import CryptContext

ctx = CryptContext(schemes=['bcrypt'])

def get_hashed_obj(obj: object) -> str:
  return ctx.hash(obj)

def verify_hashed_obj(obj: object, hashed_obj: str) -> bool:
  return ctx.verify(obj, hashed_obj)
