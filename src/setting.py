from functools import lru_cache

from pydantic import AnyHttpUrl, BaseSettings, EmailStr


class Settings(BaseSettings):
  PROJECT_NAME: str
  PROJECT_VERSION: str
  PROJECT_OWNER: dict[str, str]
  BASE_SERVER_URL: AnyHttpUrl
  
  DB_USER: str
  DB_PASSWORD: str
  DB_HOST: str
  DB_PORT: str
  DB_NAME: str
  DB_SCHEMA: str
  
  JWT_SECRET_KEY: str
  JWT_ALGORITHM: str
  # ES256_KEY: str
  # ES256_KID: str
  ACCESS_TOKEN_EXPIRY_MINUTES: int
  
  SENDGRID_EMAIL_FROM: EmailStr
  SENDGRID_NAME_FROM: str
  SENDGRID_HOST: str
  SENDGRID_API_KEY: str
  
  class Config:
    env_file = '.env'
    case_sensitive = True
    
# Reading the env file is costly, especially when read for each request. So cache the values using lru_cache.
@lru_cache()
def get_settings() -> Settings:
  return Settings()

settings = get_settings()
    
