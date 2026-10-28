from fastapi import APIRouter

from .v1 import v1_router

app_router = APIRouter(prefix="/stores")
app_router.include_router(v1_router)
