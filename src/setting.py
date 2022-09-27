from pydantic import BaseSettings


class Settings(BaseSettings):
  PROJECT_NAME: str
  PROJECT_VERSION: str
  PROJECT_OWNER: dict[str, str]
  
  DB_USER: str
  DB_PASSWORD: str
  DB_HOST: str
  DB_PORT: str
  DB_NAME: str
  DB_SCHEMA: str
  
  JWT_SECRET_KEY: str
  JWT_ALGORITHM: str
  ES256_KEY: str
  ES256_KID: str
  TOKEN_EXPIRY_IN_MINUTES: int
  
  class Config:
    env_file = '.env'
    case_sensitive = True

settings = Settings()
    
