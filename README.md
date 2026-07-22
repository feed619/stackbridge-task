# Система аутентификации и авторизации (FastAPI)

## Способ аутентификации

### Аунтефикаци реализовал через Bearer Token, чтобы можно было использовать ручки через swagger я добавил response.set_cookies (JWT Cookies) и написал свой MyOAuth2PasswordBearer который наследуется от OAuth2PasswordBearer, перегрузил метод `__call__` добавил если зоголовк Authorization пуст, то дополнительно просматриваю Cookies и достаю токен если он там есть

### Архитектура БД

#### Таблицы:

1. **users** — пользователи
   - id,
   - email
   - hashed_password
   - is_admin
   - first_name
   - last_name
   - middle_name
   - is_active
   - created_at
   - updated_at

2. **sessions** — сессии пользователей
   - id
   - user_id
   - expires_at
   - created_at

3. **roles** — роли пользователей
   - id
   - name
   - description
   - created_at

4. **endpoints** — эндпоинты
   - id
   - name
   - description
   - created_at

5. **access_rules** — правила доступа
   - id
   - role_id
   - endpoint_id
   - read_permission, read_all_permission
   - create_permission
   - update_permission, update_all_permission
   - delete_permission, delete_all_permission
   - created_at, updated_at

6. **user_roles** — назначение ролей пользователям
   - user_id
   - role_id

### Модель прав доступа

- **read_permission** - чтение ресурса
- **read_all_permission** - чтение всех записей
- **create_permission** - создание записей
- **update_permission** - обновление своих записей
- **update_all_permission** - обновление всех записей
- **delete_permission** - удаление своих записей
- **delete_all_permission** - удаление всех записей

### Тестовые роли и права

#### 1. Admin (admin@example.com / admin)

- Полный доступ ко всем ресурсам
- Может управлять ролями и правами

#### 2. Manager (manager@example.com / manager)

- Продукты: полный доступ (CRUD)
- Заказы: чтение всех, создание, обновление своих
- Пользователи: только чтение

#### 3. User (user@example.com / user)

- Продукты: только чтение
- Заказы: чтение своих, создание, обновление/удаление своих

#### 4. Guest

- Продукты: только чтение

## API Endpoints

### Установка

## Скачать

```bash
git clone https://github.com/feed619/stackbridge-task
```

## Поднять

```bash
docker compose up
```

# Много не тестировал, так что надеюсь, ошибок нет.
