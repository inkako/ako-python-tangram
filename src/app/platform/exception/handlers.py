from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.platform.exception.exceptions import BizException
from app.platform.logging import get_logger

logger = get_logger(__name__)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """
    Request validation exception handler.
    """
    logger.warning(
        f"Request validation error on {request.method} {request.url.path}: {exc}",
        # exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "message": "Invalid request. Please check your request and try again."
        },
    )


async def biz_exception_handler(request: Request, exc: BizException):
    """
    Business exception handler.
    """
    logger.warning(
        f"Biz exception on {request.method} {request.url.path} {type(exc).__name__}: {exc}",
        # exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": exc.code,
            "message": str(exc),
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Unhandled exception handler.
    """
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {exc}",
        # exc_info=exc,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error. Please try again later."},
    )
