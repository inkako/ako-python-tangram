from fastapi import APIRouter

from .v1 import v1_router

app_router = APIRouter(prefix="/api")
app_router.include_router(v1_router)
