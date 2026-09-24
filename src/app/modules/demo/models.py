from app.platform.database.base import Base, SoftDeletionMixin, TimestampMixin, UUIDMixin


class Demo(UUIDMixin, TimestampMixin, SoftDeletionMixin, Base):
    __tablename__ = "demo"
