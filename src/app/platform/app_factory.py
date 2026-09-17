from app.platform.config.settings import Settings
from fastapi import FastAPI, APIRouter


def create_app(
        router: APIRouter,
        settings: Settings | None = None,
) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
