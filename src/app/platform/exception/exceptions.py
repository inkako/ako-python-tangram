from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from starlette import status


# ------------------------------ Domain Errors ------------------------------
class DomainError(Exception):
    """A Base exception class for business logic errors in the domain layer.

    This is for domain-level errors, such as invalid business rules, domain
    constraint violations, and workflow errors. Not for HTTP protocol errors.
    """

    def __init__(
            self,
            code: str,
            message: str,
            request_id: str | None = None,
    ):
        self.code = code
        self.request_id = request_id
        super().__init__(message)


# ------------------------------ HTTP Errors ------------------------------
class CustomException(HTTPException):
    """A Base HTTP exception you can raise in your own code to show errors to the client.

    This is for client errors, invalid authentication, invalid data, etc. Not for server
    errors in your code.
    """

    def __init__(
            self,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail: Any = None,
            headers: dict[str, str] | None = None,
    ):
        if not detail:
            detail = HTTPStatus(status_code).description
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class BadRequestException(CustomException):
    def __int__(self, detail: str | None = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFoundException(CustomException):
    def __init__(self, detail: str | None = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateValueException(CustomException):
    def __init__(self, detail: str | None = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=detail)
