from app.platform.exception.exceptions import BizError


class UnauthenticatedError(BizError):
    pass

class UserExistsError(BizError):
    pass