from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, db: AsyncSession, model_id: int):
        query = select(cls.model).filter_by(id=model_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, db: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, db: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_all_ids(cls, db: AsyncSession, **filter_by):
        query = select(cls.model.id).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_all_by_with_parameters(cls, db: AsyncSession, parameters, **filter_by):
        selected_columns = []
        for param in parameters:
            if hasattr(cls.model, param):
                selected_columns.append(getattr(cls.model, param))

        if not selected_columns:
            query = select(cls.model)
        else:
            query = select(*selected_columns)

        if filter_by:
            query = query.filter_by(**filter_by)

        result = await db.execute(query)
        # return result.scalars().all()
        rows = result.all()
        return [dict(zip(parameters, row)) for row in rows]

    @classmethod
    async def add(cls, db: AsyncSession, commit: bool = True, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await db.execute(query)
        if commit:
            await db.commit()
        return result.scalar_one()

    @classmethod
    async def delete(cls, db: AsyncSession, model_id):
        query = delete(cls.model).where(cls.model.id == model_id)
        await db.execute(query)
        await db.commit()

    @classmethod
    async def update(cls, db: AsyncSession, model_id, **data):
        query = update(cls.model).where(cls.model.id == model_id).values(**data)
        await db.execute(query)
        await db.commit()

    @classmethod
    async def get_model_with_relationship(
        cls,
        db: AsyncSession,
        relationships: list[str] = None,
        all=False,
        **filter_by,
    ):
        query = select(cls.model).filter_by(**filter_by)
        if relationships:
            for rel in relationships:
                query = query.options(joinedload(getattr(cls.model, rel)))

        result = await db.execute(query)
        if all:
            return result.scalars().all()
        return result.scalar_one_or_none()
