from asyncpg import Record

from ..models.channels import Channel
from .base import BaseDao
from ..errors import EntityDoesNotExist
from . import queries


class ChannelDao(BaseDao):
    async def get_channel_by_id(self, *, channel_id: int) -> Channel:
        rows: Record = await queries.get_channel_by_id(self.connection, channel_id=channel_id)
        if rows:
            return Channel(**rows)
        raise EntityDoesNotExist
