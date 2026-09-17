from app.platform.logging import get_logger
from fastapi import APIRouter

demo_router = APIRouter()

logger = get_logger(__name__)

@demo_router.get("/demo")
def demo():
    logger.info("Demo endpoint accessed")
    return {"Hello": "World"}
