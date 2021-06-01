from fastapi import Request, Depends, HTTPException

from ..models.users import UserJWT, UserInternal
import src.strings as strings
from ..dao.users import UserDao
from ..dao.permissions import PermissionDao
from ..dependencies.dao import get_dao
from ..errors import EntityDoesNotExist
from ..utils.jwt_ import JWTUtil


async def check_permission(*, user_id: int, channel_id: int, minimum_role: int,
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao))) -> None:

    try:
        await permissionDao.check_permission(
            user_id=user_id, channel_id=channel_id, minimum_role=minimum_role)
    except EntityDoesNotExist:
        raise HTTPException(status_code=403, detail=strings.PERMISSION_ERROR02)


async def verify_token(*, request: Request, userDao: UserDao = Depends(get_dao(UserDao))
    ) -> UserJWT:
    jwtUser: JWTUtil
    try:
        jwtUser = JWTUtil.from_header(request.headers)
        jwtUser.check()
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

    try:
        await userDao.check_user(user=jwtUser.get_user())
    except EntityDoesNotExist:
        raise HTTPException(status_code=403, detail=strings.TOKEN_ERROR04)

    return jwtUser.get_user()


async def verify_token_internal(*, request: Request, userDao: UserDao = Depends(get_dao(UserDao))
    ) -> UserInternal:
    jwtUser: JWTUtil
    try:
        jwtUser = JWTUtil.from_header(request.headers)
        jwtUser.check()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        return await userDao.get_user_by_user_jwt(user=jwtUser.get_user())
    except EntityDoesNotExist:
        raise HTTPException(status_code=400, detail=strings.TOKEN_ERROR04)
