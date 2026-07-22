from app.dao.base import BaseDAO
from app.database.models import Endpoint


class EndpointDAO(BaseDAO):
    model = Endpoint
