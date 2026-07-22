from fastapi import APIRouter
from app.api.routes.admin import router as admin_router
from app.api.routes.users import router as user_router
from app.api.routes.auth import router as auth_router
from app.api.routes.products import router as products_router
from app.api.routes.orders import router as orders_router
from app.api.routes.permissions import router as permissions_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=["Авторизация"])
api_router.include_router(user_router, tags=["Пользователи"])
api_router.include_router(permissions_router, tags=["Права доступа"])
api_router.include_router(products_router, prefix="/products", tags=["Продукты"])
api_router.include_router(orders_router, prefix="/orders", tags=["Заказы"])
api_router.include_router(admin_router, tags=["Админка"])
