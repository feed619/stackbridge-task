from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.dao.access_rules import AccessRuleDAO
from app.dao.endpoints import EndpointDAO
from app.dao.roles import RoleDAO
from app.dao.users import UserDAO, UserRolesDAO
from app.schemas.permissions import *
from app.services.auth import get_current_admin, get_current_user
from app.database.dependency import get_db_async
from app.database.models import User
from .admin import router as admin_router

router = APIRouter()


@admin_router.get("/permissions/roles", description="Получении списка ролей")
async def get_roles(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> list[RoleResponse]:
    roles = await RoleDAO.find_all(db=db)
    return roles


@admin_router.post("/permissions/roles", description="Создание роли")
async def add_roles(
    role_data: RoleCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> RoleResponse:
    exist_role = await RoleDAO.find_one_or_none(db=db, name=role_data.name)
    if exist_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Роль с таким названием уже существует",
        )
    role = await RoleDAO.add(
        db=db,
        name=role_data.name,
        description=role_data.description,
    )
    return role


@admin_router.put("/permissions/roles/{role_id}", description="Обновление роли")
async def update_roles(
    role_id: UUID,
    role_data: RoleUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    role = await RoleDAO.find_by_id(db=db, model_id=role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")

    update_data = {}
    for key, value in role_data:
        if value:
            update_data[key] = value
    if update_data:
        await RoleDAO.update(db=db, model_id=role_id, **update_data)

    return {"status": "success"}


@admin_router.delete("/permissions/roles/{role_id}", description="Удаление роли")
async def delete_role(
    role_id: UUID,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    role = await RoleDAO.find_by_id(db=db, model_id=role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роль не найдена")

    await RoleDAO.delete(db=db, model_id=role_id)
    return {"status": "success"}


@admin_router.get("/permissions/endpoints", description="Получении списка endpoints")
async def get_endpoints(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> list[EndpointResponse]:
    roles = await EndpointDAO.find_all(db=db)
    return roles


@admin_router.post("/permissions/endpoints", description="Создание endpoints")
async def add_endpoints(
    endpoint_data: EndpointCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> EndpointResponse:
    exist_endpoint = await EndpointDAO.find_one_or_none(db=db, name=endpoint_data.name)
    if exist_endpoint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Эндпоинт с таким названием уже существует",
        )

    endpoint = await EndpointDAO.add(
        db=db,
        name=endpoint_data.name,
        description=endpoint_data.description,
    )
    return endpoint


@admin_router.put("/permissions/endpoints/{endpoint_id}", description="Обновление endpoint")
async def update_endpoints(
    endpoint_id: UUID,
    endpoint_data: EndpointUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    endpoint = await EndpointDAO.find_by_id(db=db, model_id=endpoint_id)
    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Эндпоинт не нейден")

    update_data = {}
    for key, value in endpoint_data:
        if value:
            update_data[key] = value
    if update_data:
        await EndpointDAO.update(db=db, model_id=endpoint_id, **update_data)

    return {"status": "success"}


@admin_router.delete("/permissions/roles/{endpoint_id}", description="Удаление endpoint")
async def delete_endpoint(
    endpoint_id: UUID,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    endpoint = await EndpointDAO.find_by_id(db=db, model_id=endpoint_id)
    if not endpoint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Эндпоинт не нейден")

    await EndpointDAO.delete(db=db, model_id=endpoint_id)
    return {"status": "success"}


@admin_router.get("/permissions/access_rules", description="Получении списка прав доступа")
async def get_access_rules(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> list[AccessRuleResponse]:
    access_rules = await AccessRuleDAO.find_all(db=db)
    return access_rules


@admin_router.post("/permissions/access_rules", description="Добавление прав доступа")
async def add_access_rules(
    access_rule_data: AccessRuleCreate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> AccessRuleResponse:
    access_rule = await AccessRuleDAO.find_one_or_none(
        db=db,
        role_id=access_rule_data.role_id,
        endpoint_id=access_rule_data.endpoint_id,
    )
    if access_rule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Права доступа для этого эндпоинта и роли уже существуют",
        )

    access_rule = await AccessRuleDAO.add(db=db, **access_rule_data)
    return access_rule


@admin_router.put("/permissions/access_rules/{access_rule_id}", description="Обновление прав доступа")
async def update_access_rules(
    access_rule_id: UUID,
    access_rule_data: AccessRuleUpdate,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    access_rule = await AccessRuleDAO.find_by_id(db=db, model_id=access_rule_id)
    if not access_rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Права доступа не найдены")

    update_data = {}
    for key, value in access_rule_data:
        if value:
            update_data[key] = value
    if update_data:
        await AccessRuleDAO.update(db=db, model_id=access_rule_id, **update_data)

    return {"status": "success"}


@admin_router.delete("/permissions/roles/{access_rule_id}", description="Удаление прав доступа")
async def delete_access_rules(
    access_rule_id: UUID,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    access_rule = await AccessRuleDAO.find_by_id(db=db, model_id=access_rule_id)
    if not access_rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Права доступа не найдены")

    await AccessRuleDAO.delete(db=db, model_id=access_rule_id)
    return {"status": "success"}


@admin_router.get("/permissions/user_role", description="Получении списка связей пользователей с ролями")
async def get_user_role(
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> list[UserRoleBase]:
    list_user_role = await UserRolesDAO.find_all(db=db)
    return list_user_role


@admin_router.post("/permissions/user_role", description="Добавление свзязи пользователь-роль")
async def add_user_role(
    user_role_data: UserRoleBase,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> UserRoleBase:
    user = await UserDAO.find_by_id(
        db=db,
        model_id=user_role_data.user_id,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с таким user_id не существует",
        )
    role = await RoleDAO.find_by_id(
        db=db,
        model_id=user_role_data.role_id,
    )
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Роль с таким role_id не существует",
        )

    exist_user_role = await UserRolesDAO.find_one_or_none(
        db=db,
        user_id=user_role_data.user_id,
        role_id=user_role_data.role_id,
    )
    if exist_user_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"У пользователя такая роль уже существует",
        )
    user_role = await UserRolesDAO.add(db=db, **user_role_data)
    return user_role


@admin_router.get("/permissions/user_role/{user_id}", description="Получени роли пользователя")
async def get_user_role(
    user_id: UUID,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> UserRoleBase:
    user_roles = await UserRolesDAO.find_one_or_none(db=db, user_id=user_id)
    if not user_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"У пользователя с таким user_id не существует роли",
        )

    return user_roles


@admin_router.patch("/permissions/user_role/{user_id}", description="Обновление роли пользователя")
async def update_user_role(
    user_id: UUID,
    role_id: UUID,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> UserRoleBase:
    user_roles = await UserRolesDAO.find_one_or_none(db=db, user_id=user_id)
    if not user_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"У пользователя с таким user_id не существует такой роли",
        )
    role = await RoleDAO.find_by_id(
        db=db,
        model_id=role_id,
    )
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Роль с таким role_id не существует",
        )
    user_roles = await UserRolesDAO.update(db=db, user_id=user_id, role_id=role_id)

    return user_roles


@admin_router.delete("/permissions/user_role/{user_id}", description="Удаление связи пользователя с ролью")
async def delete_access_user_role(
    user_id: UUID,
    role_id: UUID,
    admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    user_role = await UserRolesDAO.find_one_or_none(
        db=db,
        user_id=user_id,
        role_id=role_id,
    )
    if not user_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="У пользователя нет такой роли")
    await UserRolesDAO.delete(db=db, user_id=user_id, role_id=role_id)
    return {"status": "success"}


@router.get("/permissions/my", description="Получени своих список role_id ")
async def get_my_roles(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> Optional[UUID]:
    user_role = await UserRolesDAO.find_one_or_none(db=db, user_id=user.id)
    if not user_role:
        return None
    return user_role.role_id
