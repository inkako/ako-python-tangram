from collections.abc import Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[
ModelType,
CreateSchemaType: BaseModel,
UpdateSchemaType: BaseModel,
]:
    def __init__(self, model: type[ModelType]):
        self._model = model

    async def create(
            self,
            session: AsyncSession,
            create_schema: CreateSchemaType,
    ) -> ModelType:
        """
        Create a new record in the database.

        Args:
            session (AsyncSession): The database session.
            create_schema (CreateSchemaType): The schema for creating the record.

        Returns:
            ModelType: The created record.
        """
        create_data = create_schema.model_dump()
        db_obj = self._model(**create_data)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def get(
            self,
            session: AsyncSession,
            *args,
            **kwargs,
    ) -> ModelType | None:
        """
        Get a record.

        Args:
            session (AsyncSession): The database session.
            *args: Filter criteria. (e.g: .filter(User.name == "Alice", User.age > 18), operator overload)
            **kwargs: Filter equal conditions. (e.g: .filter_by(name="Alice", age=18)

        Returns:
            ModelType | None: The record if found, otherwise None.
        """
        stmt = select(self._model).filter(*args).filter_by(**kwargs)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_all(
            self,
            session: AsyncSession,
            *args,
            **kwargs,
    ) -> Sequence[ModelType]:
        """
        Get all records that match the given criteria.

        Args:
            session (AsyncSession): The database session.
            *args: Filter criteria. (e.g: .filter(User.name == "Alice", User.age > 18))
            **kwargs: Filter equal conditions. (e.g: .filter_by(name="Alice", age=18)

        Returns:
            Sequence[ModelType]: The list of records.
        """
        stmt = select(self._model).filter(*args).filter_by(**kwargs)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_multi(
            self,
            session: AsyncSession,
            *args,
            offset: int = 0,
            limit: int = 20,
            **kwargs,
    ) -> Sequence[ModelType]:
        """
        Get multiple records that match the given criteria.

        Args:
            session (AsyncSession): The database session.
            *args: Filter criteria. (e.g: .filter(User.name == "Alice", User.age > 18))
            offset (int): The offset for pagination.
            limit (int): The limit for pagination.
            **kwargs: Filter equal conditions. (e.g: .filter_by(name="Alice", age=18)

        Returns:
            list[ModelType]: The list of records.
        """
        stmt = (
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update(
            self,
            session: AsyncSession,
            *,
            update_schema: UpdateSchemaType,
            db_obj: ModelType | None = None,
            **kwargs,
    ) -> ModelType | None:
        """
        Update a record.

        Args:
            session (AsyncSession): The database session.
            update_schema (UpdateSchemaType): The schema for updating the record.
            db_obj (ModelType | None): The record to update.
            **kwargs: Filter equal conditions. (e.g: .filter_by(name="Alice", age=18)

        Returns:
            ModelType | None: The updated record if found, otherwise None.
        """
        db_obj = db_obj or await self.get(session, **kwargs)

        if db_obj is not None:
            update_data = update_schema.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    async def exists(
            self,
            session: AsyncSession,
            *args,
            **kwargs,
    ) -> bool:
        return await self.get(session, *args, **kwargs) is not None

    async def delete(
            self,
            session: AsyncSession,
            *args,
            db_obj: ModelType | None = None,
            **kwargs,
    ):
        db_obj = db_obj or await self.get(session, *args, **kwargs)

        await session.delete(db_obj)
        await session.commit()

        return db_obj
