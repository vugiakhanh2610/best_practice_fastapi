from os import environ
from dotenv import load_dotenv
load_dotenv()

class CoreSetting:
  PROJECT_NAME = environ.get("PROJECT_NAME")
  PROJECT_VERSION = environ.get("PROJECT_VERSION")  
  
  DB_CONNECTION_STR = environ.get('DB_CONNECTION_STR')

Setting = CoreSetting()