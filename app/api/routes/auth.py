from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.sessions import SessionDAO
from app.dao.users import UserDAO
from app.database.dependency import get_db_async
from app.database.models import User
from app.schemas.token import Token
from app.schemas.users import UserCreate, UserResponse
from app.utils.exceptions import IncorrectUserDataException, UserDeactivateException
from app.services.auth import authenticate_user, create_access_token, get_current_session, get_current_user, get_password_hash

from config import settings

router = APIRouter(prefix="/auth")


@router.post("/register", description="Регистрациия аккаунта")
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db_async),
) -> UserResponse:
    user: User = await UserDAO.find_one_or_none(db=db, email=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Такой email уже используется")

    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(
        db=db,
        email=user_data.email,
        hashed_password=hashed_password,
        is_admin=False,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
    )
    return new_user


@router.post("/login", description="Аутентификация пользователя")
async def login(
    response: Response,
    user_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_async),
) -> Token:
    user = await authenticate_user(db=db, email=user_data.username, password=user_data.password)
    if not user:
        raise IncorrectUserDataException
    if not user.is_active:
        raise UserDeactivateException

    expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    session = await SessionDAO.add(
        db=db,
        user_id=user.id,
        expires_at=expires_at,
    )
    access_token = create_access_token(user_id=str(user.id), session_id=str(session.id))
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=expires_at,
        samesite="none",
        secure=True,
        httponly=True,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", description="Выход пользователя")
async def logout(
    response: Response,
    session: Session = Depends(get_current_session),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    response.delete_cookie(key="access_token", path="/", samesite="none", secure=True, httponly=True)
    await SessionDAO.delete(db=db, model_id=session.id)
    return {"message": "Successfully logged out"}


@router.post("/logout/all", description="Выход пользователя со всех сессий")
async def logout(
    response: Response,
    session: Session = Depends(get_current_session),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    response.delete_cookie(key="access_token", path="/", samesite="none", secure=True, httponly=True)
    await SessionDAO.delete_all(db=db, user_id=session.user_id)
    return {"message": "Successfully logged out"}


@router.delete("/delete", description="Удаления аккаунта")
async def delete_account(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_async),
) -> dict:
    await UserDAO.update(db=db, model_id=user.id, is_active=False)
    await SessionDAO.delete_all(db=db, user_id=user.id)
    return {"message": "Successfully delete account"}
