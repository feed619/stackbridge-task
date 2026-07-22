import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from app.dao.users import UserRolesDAO
from app.services.auth import get_current_user
from app.database.dependency import get_db_async
from app.database.models import User

router = APIRouter()


@router.get("/", description="Получении orders")
async def get_orders(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> list:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="orders",
        action="read_all_permission",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )

    return ["order 1", "order 2", "order 3"]


@router.get("/{order_id}", description="Получении order по id")
async def get_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="orders",
        action="read_permission",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )

    return {
        "status": "success",
        "items": [
            {
                "id": 1,
                "product_id": 2,
                "product_name": "Сметана",
                "quantity": 1,
                "price": 99.99,
                "total": 99.99,
            }
        ],
    }


@router.put("/{order_id}", description="Обновление order")
async def update_orders(
    order_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="orders",
        action="update_permission",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )
    return {"status": "success"}


@router.delete("/{order_id}", description="удаление orders")
async def delete_orders(
    order_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> list:
    has_permission = await UserRolesDAO.user_has_permission(
        db=db,
        user_id=user.id,
        endpoint_name="orders",
        action="delete_permission",
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен",
        )

    return {"status": "success"}
