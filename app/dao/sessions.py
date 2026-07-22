from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.database.models import Session


class SessionDAO(BaseDAO):
    model = Session

    @classmethod
    async def delete_all(cls, db: AsyncSession, user_id):
        query = delete(cls.model).where(cls.model.user_id == user_id)
        await db.execute(query)
        await db.commit()
