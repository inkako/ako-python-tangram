from fastapi import APIRouter

from app.platform.logging import get_logger

demo_router = APIRouter()

logger = get_logger(__name__)

@demo_router.get("/demo")
def demo():
    logger.info("Demo endpoint completed")
    value = 1 / 0
    return {"Hello": "World"}
