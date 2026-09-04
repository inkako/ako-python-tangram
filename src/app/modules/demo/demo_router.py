from fastapi import APIRouter

router = APIRouter()


@router.get("/demo")
def demo_router():
    return {"Hello": "World"}
