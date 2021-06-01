from typing import List

from asyncpg import Record

from ..models.permissions import Permission
from .base import BaseDao
from ..errors import EntityDoesNotExist
from . import queries


class PermissionDao(BaseDao):
    # ToDo: rename
    async def get_user_permissions_from_id(self, *, user_id: int) -> List[Permission]:
        rows: Record = await queries.get_user_permissions_from_id(self.connection, user_id=user_id)
        if rows:
            return [Permission(**i) for i in rows]
        raise EntityDoesNotExist

    # ToDo: rename
    async def check_permission(self, *, user_id: int, channel_id: int, minimum_role: int) -> None:
        rows: Record = await queries.check_permission(self.connection,
            user_id=user_id, channel_id=channel_id, minimum_role=minimum_role)
        if rows:
            return
        raise EntityDoesNotExist

    # ToDo: rename
    async def get_user_permission(self, *, user_id: int, channel_id: int) -> int:
        rows: Record = await queries.get_user_permission(self.connection, user_id=user_id, channel_id=channel_id)
        if rows:
            return rows.get("role_id")
        raise EntityDoesNotExist

    # ToDo: rename
    async def check_permission_from_message_id(self, *, user_id: int, message_id: int, role_id: int) -> None:
        rows: Record = await queries.check_permission_from_message_id(self.connection,
            user_id=user_id, message_id=message_id, role_id=role_id)
        if rows:
            return
        raise EntityDoesNotExist
        
    async def check_user_is_owner(self, *, user_id: int, message_id: int) -> None:
        rows: Record = await queries.check_user_is_owner(self.connection,
            user_id=user_id, message_id=message_id)
        if rows:
            return
        raise EntityDoesNotExist

    async def set_permission(self, *, user_id: int, channel_id: int, role_id: int) -> None:
        await queries.set_permission(self.connection, user_id=user_id, channel_id=channel_id, role_id=role_id)

    async def create_permission(self, *, user_id: int, channel_id: int) -> None:
        await queries.create_permission(self.connection, user_id=user_id, channel_id=channel_id)

    async def check_mod_privileges(self, *, user_id: int, message_id: int) -> None:
        rows: Record = await queries.check_mod_privileges(self.connection, user_id=user_id, message_id=message_id)
        if rows:
            return
        raise EntityDoesNotExist
