class BizError(Exception):
    """Base exception class for business logic errors."""

    def __init__(self, code: str, message: str | None):
        self.code = code
        super().__init__(message)


class UserExistsError(BizError):
    pass
