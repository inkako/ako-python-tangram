from app.platform.authn.models import User
from app.platform.authn.schemas import UserCreateSchema, UserUpdateSchema
from app.platform.repository.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]): ...
