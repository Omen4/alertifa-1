from asyncpg import Record

from ..models.channels import Channel
from ..models.users import UserInMessage
from ..models.messages import MessageInResponse
from .base import BaseDao
from ..errors import EntityDoesNotExist
from . import queries


class MessageDao(BaseDao):
    async def create(self, *, channel_id: int, user_id: int, body: str) -> None:
        await queries.create_message(self.connection, channel_id=channel_id, user_id=user_id, body=body)

    async def update(self, *, message_id: int, body: str) -> None:
        await queries.update_message(self.connection, message_id=message_id, body=body)

    async def delete(self, *, message_id: int) -> None:
        await queries.delete_message(self.connection, message_id=message_id)

    async def read(self, *, message_id: int) -> MessageInResponse:
        rows: Record = await queries.read_message(self.connection, message_id=message_id)
        if rows:
            return MessageInResponse(
                user=UserInMessage(
                    user_id=rows.get("user_id"),
                    user_name=rows.get("user_name")
                ),
                channel=Channel(
                    channel_id=rows.get("channel_id"),
                    channel_name=rows.get("channel_name")
                ),
                created_at=rows.get("created_at"),
                updated_at=rows.get("updated_at"),
                body=rows.get("body")
            )
        raise EntityDoesNotExist
