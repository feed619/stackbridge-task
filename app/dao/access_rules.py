from app.dao.base import BaseDAO
from app.database.models import AccessRule


class AccessRuleDAO(BaseDAO):
    model = AccessRule
