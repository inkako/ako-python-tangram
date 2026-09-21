from app.platform.constant.enums import AccountStatusEnum
from app.platform.database.base import Base, SoftDeletionMixin, TimestampMixin
from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column


class User(TimestampMixin, SoftDeletionMixin, Base):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
        init=False,
    )

    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))
    account_status: Mapped[int] = mapped_column(
        SmallInteger,
        default=AccountStatusEnum.ACTIVE,
        nullable=False,
    )
