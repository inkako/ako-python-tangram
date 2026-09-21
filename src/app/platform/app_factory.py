from app.platform.config.settings import get_settings
from app.platform.exception.exceptions import BizException
from app.platform.exception.handlers import (
    biz_exception_handler,
    request_validation_exception_handler,
    unhandled_exception_handler,
)
from app.platform.logging import get_logger
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError

logger = get_logger(__name__)

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

    logger.debug("middlewares registered")


def _register_exception_handlers(app: FastAPI):
    """
    Register all exception handlers.
    """
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    logger.debug("exception handlers registered")


def create_app(router: APIRouter) -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    _register_middlewares(app)
    _register_exception_handlers(app)

    return app
