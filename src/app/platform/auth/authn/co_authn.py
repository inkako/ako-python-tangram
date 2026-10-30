

from app.platform.auth.users.models import User
from app.platform.auth.users.repository import UserRepository
from app.platform.logging import get_logger

logger = get_logger(__name__)

userRepo = UserRepository(User)


class CoAuthn:
    def __int__(self):
        ...


co_authn = CoAuthn(

)


def get_co_authn() -> CoAuthn:
    return co_authn
