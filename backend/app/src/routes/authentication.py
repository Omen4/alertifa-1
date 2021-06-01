from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from ..dependencies.dao import get_dao
from ..utils.jwt_ import JWTUtil
from ..dao.users import UserDao
from ..errors import EntityDoesNotExist
from ..models.users import (
    UserInCreate,
    UserInLogin,
    UserWithToken,
    UserInternal,
    UserJWT
)
from .. import strings


router = APIRouter()


# possibilité d'amélioration: log par mail+pwd, pseudo+pwd, uid+pwd
@router.post("/login", response_model=UserWithToken, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    userDao: UserDao = Depends(get_dao(UserDao)),
) -> UserWithToken:
    try:
        user: UserInternal = await userDao.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR01
        )
    if not user.check_password(user_login.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR02
        )
    jwt_id: int = await userDao.invalidate_previous_token(user=user)
    user.jwt_id = jwt_id
    jwtUser: JWTUtil = JWTUtil.from_user(user)
    return jwtUser.get_user_with_token()


@router.post("", status_code=HTTP_201_CREATED, response_model=UserWithToken, name="auth:register")
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    userDao: UserDao = Depends(get_dao(UserDao))
) -> UserWithToken:
    try:
        await userDao.get_user_by_username(user_name=user_create.user_name)
    except EntityDoesNotExist:
        pass
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR05
        )

    try:
        await userDao.get_user_by_email(email=user_create.email)
    except EntityDoesNotExist:
        pass
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.LOGIN_ERROR04
        )

    user: UserJWT = await userDao.create_user(**user_create.dict())
    jwtUser: JWTUtil = JWTUtil.from_user(user)
    return jwtUser.get_user_with_token()
