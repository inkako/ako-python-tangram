from starlette import status

from app.platform.exception import CustomException


class UnauthenticatedException(CustomException):
    def __init__(self, detail: str | None = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(CustomException):
    def __init__(self, detail: str | None = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class CSRFException(CustomException):
    """Raised when CSRF validation fails on an unsafe (mutating) request."""

    def __init__(self, detail: str = "CSRF token validation failed"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers={"X-CSRF-Error": "true"},
        )
