from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.platform.constant.enums import AccountStatusEnum
from app.platform.database.base import Base, SoftDeletionMixin, TimestampMixin


class User(TimestampMixin, SoftDeletionMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        init=False,
    )

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False,
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    account_status: Mapped[int] = mapped_column(
        SmallInteger,
        default=AccountStatusEnum.ACTIVE,
        nullable=False,
    )

