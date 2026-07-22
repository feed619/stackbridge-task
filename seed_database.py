"""
Скрипт для заполнения базы данных тестовыми данными
Запуск: python seed_database.py
"""

import asyncio
import uuid
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text

from app.dao.access_rules import AccessRuleDAO
from app.dao.endpoints import EndpointDAO
from app.dao.users import UserDAO, UserRolesDAO
from app.dao.roles import RoleDAO
from app.database.dependency import AsyncSession, AsyncSessionLocal
from app.database.models import User, Role, AccessRule, Endpoint, Session, UserRoles
from app.services.auth import get_password_hash

USERS = [
    {
        "email": "admin@example.com",
        "password": "admin",
        "first_name": "Админ",
        "last_name": "Администраторов",
        "middle_name": "Алексеевич",
        "is_active": True,
        "is_admin": True,
    },
    {
        "email": "manager@example.com",
        "password": "manager",
        "first_name": "Менеджер",
        "last_name": "Менеджеров",
        "middle_name": "Петрович",
        "is_active": True,
        "is_admin": False,
    },
    {
        "email": "user@example.com",
        "password": "user",
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "is_active": True,
        "is_admin": False,
    },
    {
        "email": "seller@example.com",
        "password": "seller",
        "first_name": "Сергей",
        "last_name": "Сергеев",
        "middle_name": "Сергеевич",
        "is_active": True,
        "is_admin": False,
    },
]

ROLES = [
    {"name": "admin", "description": "Администратор системы - имеет полный доступ ко всем ресурсам"},
    {"name": "manager", "description": "Менеджер - управление товарами и заказами"},
    {"name": "user", "description": "Обычный пользователь - базовые права"},
    {"name": "guest", "description": "Гость - только чтение товаров"},
    {"name": "seller", "description": "Продавец - управление своими товарами"},
]

ENDPOINTS = [
    {"name": "users", "description": "Пользователи системы"},
    {"name": "products", "description": "Товары"},
    {"name": "orders", "description": "Заказы"},
    {"name": "permissions", "description": "Права доступа"},
]


ACCESS_RULES = [
    (
        "admin",
        "users",
        {
            "read": True,
            "read_all": True,
            "create": True,
            "update": True,
            "update_all": True,
            "delete": True,
            "delete_all": True,
        },
    ),
    (
        "admin",
        "products",
        {
            "read": True,
            "read_all": True,
            "create": True,
            "update": True,
            "update_all": True,
            "delete": True,
            "delete_all": True,
        },
    ),
    (
        "admin",
        "orders",
        {
            "read": True,
            "read_all": True,
            "create": True,
            "update": True,
            "update_all": True,
            "delete": True,
            "delete_all": True,
        },
    ),
    (
        "admin",
        "permissions",
        {
            "read": True,
            "read_all": True,
            "create": True,
            "update": True,
            "update_all": True,
            "delete": True,
            "delete_all": True,
        },
    ),
    (
        "manager",
        "users",
        {
            "read": True,
            "read_all": True,
            "create": False,
            "update": False,
            "update_all": False,
            "delete": False,
            "delete_all": False,
        },
    ),
    (
        "manager",
        "products",
        {
            "read": True,
            "read_all": True,
            "create": True,
            "update": True,
            "update_all": True,
            "delete": True,
            "delete_all": True,
        },
    ),
    (
        "manager",
        "orders",
        {
            "read": True,
            "read_all": True,
            "create": True,
            "update": True,
            "update_all": True,
            "delete": True,
            "delete_all": True,
        },
    ),
    (
        "user",
        "users",
        {
            "read": True,
            "read_all": False,
            "create": False,
            "update": True,
            "update_all": False,
            "delete": True,
            "delete_all": False,
        },
    ),
    (
        "user",
        "products",
        {
            "read": True,
            "read_all": True,
            "create": False,
            "update": False,
            "update_all": False,
            "delete": False,
            "delete_all": False,
        },
    ),
    (
        "user",
        "orders",
        {
            "read": True,
            "read_all": False,
            "create": True,
            "update": False,
            "update_all": False,
            "delete": False,
            "delete_all": False,
        },
    ),
    (
        "guest",
        "products",
        {
            "read": True,
            "read_all": True,
            "create": False,
            "update": False,
            "update_all": False,
            "delete": False,
            "delete_all": False,
        },
    ),
    (
        "seller",
        "products",
        {
            "read": True,
            "read_all": False,
            "create": True,
            "update": True,
            "update_all": False,
            "delete": True,
            "delete_all": False,
        },
    ),
    (
        "seller",
        "orders",
        {
            "read": True,
            "read_all": False,
            "create": False,
            "update": True,
            "update_all": False,
            "delete": False,
            "delete_all": False,
        },
    ),
]

USER_ROLES = [
    ("admin@example.com", "admin"),
    ("manager@example.com", "manager"),
    ("user@example.com", "user"),
    ("seller@example.com", "seller"),
]


async def seed_users(session: AsyncSession):
    users = {}
    for user_data in USERS:
        user = await UserDAO.add(
            db=session,
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            middle_name=user_data["middle_name"],
            hashed_password=get_password_hash(user_data["password"]),
            is_active=user_data["is_active"],
            is_admin=user_data["is_admin"],
        )
        users[user_data["email"]] = user
    print(f"Создано {len(users)} ролей")
    return users


async def seed_roles(session: AsyncSession):
    roles = {}
    for role_data in ROLES:
        role = await RoleDAO.add(
            db=session,
            name=role_data["name"],
            description=role_data["description"],
        )
        roles[role_data["name"]] = role
    print(f"Создано {len(roles)} ролей")
    return roles


async def seed_endpoints(session: AsyncSession):
    endpoints = {}
    for endpoint_data in ENDPOINTS:
        endpoint = await EndpointDAO.add(
            db=session,
            name=endpoint_data["name"],
            description=endpoint_data["description"],
        )
        endpoints[endpoint_data["name"]] = endpoint
    print(f"Создано {len(endpoints)} ресурсов")
    return endpoints


async def seed_access_rules(session: AsyncSession, roles: dict, resources: dict):
    for rule_data in ACCESS_RULES:
        role_name, enpoint_name, permissions = rule_data

        role = roles.get(role_name)
        enpoint = resources.get(enpoint_name)

        if not role or not enpoint:
            print(f"⚠️ Пропуск правила: роль {role_name} или ресурс {enpoint_name} не найдены")
            continue

        await AccessRuleDAO.add(
            db=session,
            role_id=role.id,
            endpoint_id=enpoint.id,
            read_permission=permissions.get("read", False),
            read_all_permission=permissions.get("read_all", False),
            create_permission=permissions.get("create", False),
            update_permission=permissions.get("update", False),
            update_all_permission=permissions.get("update_all", False),
            delete_permission=permissions.get("delete", False),
            delete_all_permission=permissions.get("delete_all", False),
        )

    print(f"Создано {ACCESS_RULES} правил доступа")


async def seed_user_roles(session: AsyncSession, users: dict, roles: dict):
    for email, role_name in USER_ROLES:
        user = users.get(email)
        role = roles.get(role_name)

        if not user or not role:
            print(f"⚠️  Пропуск назначения: пользователь {email} или роль {role_name} не найдены")
            continue

        user_role = await UserRolesDAO.find_one_or_none(db=session, user_id=user.id, role_id=role.id)

        if not user_role:
            await UserRolesDAO.add(
                db=session,
                user_id=user.id,
                role_id=role.id,
            )

    print(f"Назначено {USER_ROLES} ролей пользователям")


async def seed_all():
    try:
        async with AsyncSessionLocal() as session:
            admin = await UserDAO.find_one_or_none(db=session, email="admin@example.com")
            if admin:
                return
            users = await seed_users(session)
            roles = await seed_roles(session)
            resources = await seed_endpoints(session)
            await seed_access_rules(session, roles, resources)
            await seed_user_roles(session, users, roles)
            print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")

            print("Тестовые учетные записи:")
            print(" - Админ: admin@example.com / admin")
            print(" - Менеджер: manager@example.com / manager")
            print(" - Пользователь: user@example.com / user")
            print(" - Продавец: seller@example.com / seller")

    except Exception as e:
        print(f"Ошибка при заполнении БД: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(seed_all())
