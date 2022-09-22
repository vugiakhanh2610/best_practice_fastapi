from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Setting(BaseSettings):
  PROJECT_NAME: str
  PROJECT_VERSION: str
  PROJECT_OWNER: dict[str, str]
  DB_CONNECTION_STR: str
  
  class Config:
    env_file = ".env"
    case_sensitive = True
    