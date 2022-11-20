from fastapi import FastAPI

from routers import app_user_router, auth_router, group_router, module_router

PREFIX = '/api/v1'

def create_endpoints(app: FastAPI):
  app.include_router(auth_router.router)
  app.include_router(app_user_router.router, prefix=PREFIX)
  app.include_router(group_router.router, prefix=PREFIX)
  app.include_router(module_router.router, prefix=PREFIX)
