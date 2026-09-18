from app.platform.config.settings import get_settings
from fastapi import FastAPI, APIRouter

settings = get_settings()


def _register_middlewares(app):
    """
    Register all middlewares.
    """

    # Register CORS middleware
    if settings.CORS_ENABLED:
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.ALLOWED_METHODS,
            allow_headers=settings.ALLOWED_HEADERS,
        )

    # Register GZIP middleware
    if settings.GZIP_ENABLED:
        from fastapi.middleware.gzip import GZipMiddleware
        app.add_middleware(GZipMiddleware, minimum_size=settings.GZIP_MIN_SIZE)


def create_app(
        router: APIRouter
) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    _register_middlewares(app)

    return app
