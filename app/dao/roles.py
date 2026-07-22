from app.dao.base import BaseDAO
from app.database.models import Role


class RoleDAO(BaseDAO):
    model = Role
