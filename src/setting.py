from pydantic import BaseSettings


class Setting(BaseSettings):
  PROJECT_NAME: str
  PROJECT_VERSION: str
  PROJECT_OWNER: dict[str, str]
  
  DB_USER: str
  DB_PASSWORD: str
  DB_HOST: str
  DB_PORT: str
  DB_NAME: str
  DB_SCHEMA: str
  
  class Config:
    env_file = '.env'
    case_sensitive = True

setting = Setting()
    
