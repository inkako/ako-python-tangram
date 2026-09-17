from fastapi import APIRouter

from app.modules.demo.router import demo_router

v1_router = APIRouter(prefix="/v1", tags=["DEMO"])
v1_router.include_router(demo_router)
