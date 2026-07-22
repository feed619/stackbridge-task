from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.database.models import AccessRule, Endpoint, Role, User, UserRoles


class UserDAO(BaseDAO):
    model = User


class UserRolesDAO(BaseDAO):
    model = UserRoles

    @classmethod
    async def delete(cls, db: AsyncSession, user_id: UUID, role_id: UUID) -> bool:
        query = delete(cls.model).where(cls.model.user_id == user_id, cls.model.role_id == role_id)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0

    @classmethod
    async def find_all_roles(cls, db: AsyncSession, **filter_by):
        query = select(cls.model.role_id).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(cls, db: AsyncSession, user_id, role_id):
        query = update(cls.model).where(cls.model.user_id == user_id).values(role_id=role_id)
        await db.execute(query)
        await db.commit()

    @classmethod
    async def user_has_permission(
        cls,
        db: AsyncSession,
        user_id: UUID,
        endpoint_name: str,
        action: str,
    ) -> bool:

        # Получаем правило доступа
        query = (
            select(AccessRule)
            .join(Role, AccessRule.role_id == Role.id)
            .join(UserRoles, Role.id == UserRoles.role_id)
            .join(Endpoint, AccessRule.endpoint_id == Endpoint.id)
            .where(UserRoles.user_id == user_id, Endpoint.name == endpoint_name)
        )

        result = await db.execute(query)
        access_rule = result.scalars().one_or_none()

        if not access_rule:
            return False
        return getattr(access_rule, action, False)
