from typing import Any

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.auth.authn.exceptions import UnauthenticatedException
from app.platform.auth.users.models import User
from app.platform.auth.users.repository import UserRepository
from app.platform.constant.enums import AccountStatusEnum
from app.platform.logging import get_logger
from app.platform.util import canonical_utils
from app.platform.util.security_utils import verify_password

logger = get_logger(__name__)

userRepo = UserRepository(User)

class CoAuthn:
    def __int__(self):
        ...

    async def authenticate_password(self, db: AsyncSession, identifier: str, password: str) -> User:
        login_id = canonical_utils.canonical_identifier(identifier)

        user = await userRepo.get(db, username=login_id)
        if user is None:
            logger.warning("Invalid username or password, username: %s", login_id)
            raise UnauthenticatedException("Invalid username or password")

        if AccountStatusEnum.ACTIVE != user.account_status:
            logger.warning("User is not active, username: %s, account_status: %s", login_id, user.account_status)
            raise UnauthenticatedException("User is not active")

        is_passed = verify_password(password, user.password)
        if not is_passed:
            logger.warning("Invalid username or password, username: %s", login_id)
            raise UnauthenticatedException("Invalid username or password")

        return user


    async def _create_session(self):
        ...


    def _set_session_cookies(self, response, session_id):
        ...

    async def _complete_login(
        db: AsyncSession,
        identifier: str,
        password: str,
    ):
        ...

    async def password_login(self, request: Request, response: Response) -> dict[str, Any]:
        ...

def get_co_authn() -> CoAuthn:
    ...

co_authn = get_co_authn()