from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Response
from starlette.requests import Request

from app.platform.auth.authn.exceptions import UnauthenticatedException
from app.platform.auth.users.models import User
from app.platform.constant.enums import AccountStatusEnum
from app.platform.logging import get_logger
from app.platform.util import canonical_utils, verify_password

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.platform.auth.authn.hooks import AuthnHooks
    from app.platform.auth.users.service import UserService

logger = get_logger(__name__)


@dataclass
class AuthnRuntime:
    """Shared, facade-owned state handed to every transport.

    Transports are constructed by the user as lightweight config objects;
    the facade binds them to this runtime so they can reach the secret key,
    the user service, hooks, etc., without the user having to wire any of it.
    """

    secret_key: str
    user_service: "UserService"
    hooks: "AuthnHooks"

    async def authenticate_password(
            self,
            db: "AsyncSession",
            identifier: str,
            password: str,
            *,
            request: Request,
    ) -> User:
        login_id = canonical_utils.canonical_identifier(identifier)

        user = await self.user_service.get(db, username=login_id)
        if user is None:
            logger.warning("Invalid username: %s", login_id)
            raise UnauthenticatedException("Invalid username or password")

        if AccountStatusEnum.ACTIVE != user.account_status:
            logger.warning("User is not active, username: %s, account_status: %s", login_id, user.account_status)
            raise UnauthenticatedException("User is not active")

        is_passed = verify_password(password, user.password)
        if not is_passed:
            logger.warning("Invalid password, username: %s", login_id)
            raise UnauthenticatedException("Invalid username or password")

        return user


@dataclass
class AuthnContext:
    ...


class Transport(ABC):
    name: str = "_abc_transport_"

    def __init__(self, runtime: AuthnRuntime):
        self.runtime = runtime

    def contributes_routes(self) -> APIRouter | None:
        return None

    @abstractmethod
    async def complete_login(
            self,
            request: Request,
            response: Response,
            user: User,
    ) -> dict[str, Any]:
        raise NotImplementedError(f"The {self.name!r} transport doesn't issue login credentials.")
