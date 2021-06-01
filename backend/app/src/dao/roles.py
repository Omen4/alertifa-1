from asyncpg import Record

from ..models.roles import Role
from .base import BaseDao

from ..errors import EntityDoesNotExist
from . import queries


class RoleDao(BaseDao):
    async def find_by_id(self, *, role_id: int) -> Role:
        rows: Record = await queries.get_role_by_id(self.connection, role_id=role_id)
        if rows:
            return Role(**rows)
        raise EntityDoesNotExist
