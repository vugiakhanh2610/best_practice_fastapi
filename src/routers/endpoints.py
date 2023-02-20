from fastapi import FastAPI

from routers import course_router

PREFIX = '/api/v1'

def create_endpoints(app: FastAPI):
  app.include_router(course_router.router, prefix=PREFIX)
