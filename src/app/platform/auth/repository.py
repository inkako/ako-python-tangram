from app.platform.auth.models import User
from app.platform.auth.schemas import UserCreateSchema, UserUpdateSchema
from app.platform.repository.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]): ...
