from jose import jwt
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from app.dao.sessions import SessionDAO
from app.dao.users import UserDAO
from app.database.dependency import get_db_async
from app.database.models import User
from app.utils.exceptions import NotAuthenticatedException, TokenAdminException
from config import settings


class MyOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(
        self,
        tokenUrl,
        scheme_name=None,
        scopes=None,
        description=None,
        auto_error=True,
        refreshUrl=None,
    ):
        super().__init__(tokenUrl, scheme_name, scopes, description, auto_error, refreshUrl)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            access_token = request.cookies.get("access_token")
            if access_token:
                return access_token
            if self.auto_error:
                raise self.make_not_authenticated_error()
            else:
                return None
        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = MyOAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хэширование пароля"""
    return pwd_context.hash(password)


def create_access_token(user_id: str, session_id: str = None) -> str:
    """Создание access токена"""
    payload = {
        "user_id": user_id,
        "session_id": session_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_token(token: str) -> dict:
    """Декодирование JWT токена"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def get_current_session(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_async),
) -> User:
    """Получении сессии пользователя"""

    payload = decode_token(token)
    if payload is None:
        raise NotAuthenticatedException

    session_id = payload.get("session_id")
    if session_id is None:
        raise NotAuthenticatedException

    session = await SessionDAO.find_by_id(db=db, model_id=session_id)
    if session is None:
        raise NotAuthenticatedException

    if session.expires_at < datetime.now(timezone.utc):
        raise NotAuthenticatedException

    user = await UserDAO.find_by_id(db=db, model_id=session.user_id)
    if user is None or not user.is_active:
        raise NotAuthenticatedException

    return session


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_async),
) -> User:
    """Получении пользователя"""
    
    payload = decode_token(token)
    if payload is None:
        raise NotAuthenticatedException

    session_id = payload.get("session_id")
    if session_id is None:
        raise NotAuthenticatedException

    session = await SessionDAO.find_by_id(db=db, model_id=session_id)
    if session is None:
        raise NotAuthenticatedException

    if session.expires_at < datetime.now(timezone.utc):
        raise NotAuthenticatedException

    user = await UserDAO.find_by_id(db=db, model_id=session.user_id)
    if user is None or not user.is_active:
        raise NotAuthenticatedException
    return user


async def get_current_admin(
    user: str = Depends(get_current_user),
) -> User:
    """Получении Админа"""
    if not user.is_admin:
        raise TokenAdminException
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await UserDAO.find_one_or_none(db=db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
