from fastapi import FastAPI

from routers import app_user_router, role_router

PREFIX = '/api/v1'

def create_endpoints(app: FastAPI):
  app.include_router(app_user_router.router, prefix=PREFIX)
  app.include_router(role_router.router, prefix=PREFIX)
