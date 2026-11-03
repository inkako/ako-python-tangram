from app.platform.auth.users.models import User
from app.platform.auth.users.schemas import UserCreateSchema, UserUpdateSchema
from app.platform.repository import BaseRepository


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]):
    ...


user_repo = UserRepository(User)


def get_user_repo():
    return user_repo
