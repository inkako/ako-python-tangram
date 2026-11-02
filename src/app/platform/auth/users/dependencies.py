from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.auth.users.models import User
from app.platform.auth.users.repository import UserRepository
from app.platform.database.session import get_async_session

user_repo = UserRepository(User)


def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    ...
