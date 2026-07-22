from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.dao.sessions import SessionDAO
from app.dao.users import UserDAO
from app.schemas.users import UserResponse, UserUpdate
from app.services.auth import get_current_user
from app.database.dependency import get_db_async
from app.database.models import User

router = APIRouter()


@router.get("/profile", description="Получении Профиля")
async def get_profile(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> UserResponse:

    user = await UserDAO.find_by_id(db=db, model_id=user.id)
    return user


@router.put("/profile", description="Обновление аккаунта")
async def update_profile(
    user_data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    update_data = {}
    for key, value in user_data:
        if value:
            update_data[key] = value
    if update_data:
        await UserDAO.update(db=db, model_id=user.id, **update_data)
    return {"status": "success"}


@router.delete("/profile", description="Удаления аккаунта")
async def delete_account(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    await UserDAO.update(db=db, model_id=user.id, is_active=False)
    await SessionDAO.delete_all(db=db, user_id=user.id)
    return {"status": "success"}
