import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.dao.users import UserRolesDAO
from app.services.auth import get_current_user
from app.database.dependency import get_db_async
from app.database.models import User

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", description="Получении products (Может читать Гость)")
async def get_products(
    db: AsyncSession = Depends(get_db_async),
) -> list:
    return ["продукт 1", "продукт 2", "продукт 3"]


@router.get("/{product_id}", description="Получении product по id")
async def get_product(
    product_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="products",
        action="Доступ запрещен",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return {
        "name": "Сметана",
        "price": 99.99,
    }


@router.put("/{product_id}", description="Обновление product")
async def update_products(
    product_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="products",
        action="update_permission",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )

    return {"status": "success"}


@router.delete("/{product_id}", description="удаление products")
async def delete_products(
    product_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> list:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="products",
        action="delete_permission",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )

    return {"status": "success"}
