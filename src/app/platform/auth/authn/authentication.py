from app.platform.auth.models import User
from app.platform.auth.authn.repository import UserRepository
from app.platform.constant.enums import AccountStatusEnum
from app.platform.exception import biz_code
from app.platform.exception.exceptions import UnauthenticatedError
from app.platform.logging import get_logger
from app.platform.util import canonical_utils
from app.platform.util.security_utils import verify_password
from sqlalchemy.ext.asyncio import AsyncSession

logger = get_logger(__name__)

userRepo = UserRepository(User)


async def authenticate_password(db: AsyncSession, identifier: str, password: str) -> User:
    login_id = canonical_utils.canonical_identifier(identifier)

    user = await userRepo.get(db, username=login_id)
    if user is None:
        logger.warning("Invalid username or password, username: %s", login_id)
        raise UnauthenticatedError(biz_code.UNAUTHENTICATED, "Invalid username or password")

    if AccountStatusEnum.ACTIVE != user.account_status:
        logger.warning("User is not active, username: %s, account_status: %s", login_id, user.account_status)
        raise UnauthenticatedError(biz_code.UNAUTHENTICATED, "User is not active")

    is_passed = verify_password(password, user.password)
    if not is_passed:
        logger.warning("Invalid username or password, username: %s", login_id)
        raise UnauthenticatedError(biz_code.UNAUTHENTICATED, "Invalid username or password")

    return user


async def _create_session():
    ...


def _set_session_cookies(response, session_id):
    ...

async def complete_login(
    db: AsyncSession,
    identifier: str,
    password: str,
):
    ...