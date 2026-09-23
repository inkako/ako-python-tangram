from sqlalchemy.ext.asyncio import AsyncSession

from app.platform.auth.models import User
from app.platform.auth.repository import UserRepository
from app.platform.auth.schemas import UserCreateSchema
from app.platform.constant import biz_code
from app.platform.exception.exceptions import UserExistsError
from app.platform.util.security_utils import get_password_hash

userRepo = UserRepository(User)


class UserService:

    async def user_exists(self, session: AsyncSession, username: str):
        """
        Check if a user exists.
        """
        return await userRepo.exists(session, username=username)

    async def create_user(
            self,
            session: AsyncSession,
            user_create_schema: UserCreateSchema,
    ) -> User:
        """
        Create a new user.
        """
        username_exists = await userRepo.exists(session, username=user_create_schema.username)
        if username_exists:
            raise UserExistsError(biz_code.DATA_EXISTS, "Username already exists")

        email_exists = await userRepo.exists(session, email=user_create_schema.email)
        if email_exists:
            raise UserExistsError(biz_code.DATA_EXISTS, "Email already exists")

        phone_exists = await userRepo.exists(session, phone=user_create_schema.phone)
        if phone_exists:
            raise UserExistsError(biz_code.DATA_EXISTS, "Phone already exists")

        # Hash the password
        user_create_schema.password = get_password_hash(user_create_schema.password)

        created_user = await userRepo.create(session, user_create_schema)

        if not created_user:
            raise UserExistsError(biz_code.DATA_EXISTS, "Failed to create user")

        return created_user
