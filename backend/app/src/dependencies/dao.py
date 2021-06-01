from typing import AsyncGenerator, Callable, Type

from asyncpg.connection import Connection
from asyncpg.pool import Pool
from fastapi import Depends
from starlette.requests import Request

from ..dao.base import BaseDao


def _get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


async def _get_connection_from_pool(pool: Pool = Depends(_get_db_pool)) -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        yield conn


def get_dao(dao_type: Type[BaseDao]) -> Callable[[Connection], BaseDao]:
    def _get_dao(conn: Connection = Depends(_get_connection_from_pool)) -> BaseDao:
        return dao_type(conn)

    return _get_dao
