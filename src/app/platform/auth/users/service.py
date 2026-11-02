from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.auth.users.models import User
from app.platform.auth.users.schemas import UserCreateSchema
from app.platform.exception.exceptions import DuplicateValueException
from app.platform.repository.base import BaseRepository
from app.platform.util import get_password_hash


class UserService:
    def __init__(self, repository: BaseRepository):
        self.user_repo = repository

    async def user_exists(self, session: AsyncSession, username: str):
        """
        Check if a user exists.
        """
        return await self.user_repo.exists(session, username=username)

    async def create_user(
            self,
            session: AsyncSession,
            user_create_schema: UserCreateSchema,
    ) -> User:
        """
        Create a new user.
        """
        username_exists = await self.user_repo.exists(session, username=user_create_schema.username)
        if username_exists:
            raise DuplicateValueException("Account already exists")

        email_exists = await self.user_repo.exists(session, email=user_create_schema.email)
        if email_exists:
            raise DuplicateValueException("Email already exists")

        phone_exists = await self.user_repo.exists(session, phone=user_create_schema.phone)
        if phone_exists:
            raise DuplicateValueException("Phone already exists")

        # Hash the password
        user_create_schema.password = get_password_hash(user_create_schema.password)

        created_user = await self.user_repo.create(session, user_create_schema)

        await session.commit()

        return created_user

    async def get(
            self,
            session: AsyncSession,
            username: str,
    ) -> User:
        return await self.user_repo.get(session, username=username)
