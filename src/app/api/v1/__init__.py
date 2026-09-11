from fastapi import APIRouter

from app.modules.demo.demo_router import router as demo_router

router = APIRouter(prefix="/v1", tags=["DEMO"])
router.include_router(demo_router)
