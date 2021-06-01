from asyncpg import Record

from ..models.users import UserInDB, UserPublic, UserJWT, UserInternal
from .base import BaseDao
from ..errors import EntityDoesNotExist
from . import queries


class UserDao(BaseDao):
    # ToDo: rename check user from jwt?
    async def check_user(self, *, user: UserJWT) -> None:
        rows: Record = await queries.check_user(self.connection,
            user_id=user.user_id,
            user_name=user.user_name,
            email=user.email,
            jwt_id=user.jwt_id
        )
        if rows:
            return
        raise EntityDoesNotExist

    async def invalidate_previous_token(self, *, user: UserJWT) -> int:
        return await queries.invalidate_previous_token(self.connection,
            user_id=user.user_id,
            user_name=user.user_name,
            email=user.email,
            jwt_id=user.jwt_id
        )

    async def get_user_by_username(self, *, user_name: str) -> UserInDB:
        rows: Record = await queries.get_user_by_username(self.connection, user_name=user_name)
        if rows:
            return UserInDB(**rows)
        raise EntityDoesNotExist

    # ToDo: rename ~ check user sauf retourne UserInternal
    async def get_user_by_user_jwt(self, *, user: UserJWT) -> UserInternal:
        rows: Record = await queries.check_user(self.connection,
            user_id=user.user_id,
            user_name=user.user_name,
            email=user.email,
            jwt_id=user.jwt_id
        )
        if rows:
            return UserInternal(**rows)
        raise EntityDoesNotExist

    async def get_user_by_email(self, *, email: str) -> UserInternal:
        rows: Record = await queries.get_user_by_email(self.connection, email=email)
        if rows:
            return UserInternal(**rows)
        raise EntityDoesNotExist

    # ToDo: un peu hacky pour générer hash + salt
    async def create_user(self, *, user_name: str, email: str, password: str) -> UserJWT:
        user: UserInDB = UserInDB(user_name=user_name, email=email)
        user.change_password(password)
        rows: Record = await queries.create_user(
            self.connection,
            user_name=user.user_name,
            email=user.email,
            salt=user.salt,
            hashed_password=user.hashed_password,
        )
        return UserJWT(**rows)

    async def read(self, *, user_id: int) -> UserPublic:
        rows: Record = await queries.get_user_by_id(self.connection, user_id=user_id)
        if rows:
            return UserPublic(**rows)
        raise EntityDoesNotExist

    async def update_email(self, *, user_id: int, email: str) -> None:
        await queries.update_email(self.connection, user_id=user_id, email=email)

    async def update_user_name(self, *, user_id: int, user_name: str) -> None:
        await queries.update_user_name(self.connection, user_id=user_id, user_name=user_name)

    async def update_password(self, *, user: UserInternal, password: str) -> None:
        user.change_password(password)
        await queries.update_password(
            self.connection, 
            user_id=user.user_id,
            salt=user.salt,
            hashed_password=user.hashed_password
        )

    async def update_bio(self, *, user_id: int, bio: str) -> None:
        await queries.update_bio(self.connection, user_id=user_id, bio=bio)
