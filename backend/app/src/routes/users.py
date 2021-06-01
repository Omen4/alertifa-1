from fastapi import APIRouter, Body, Depends, Path, HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from ..models.users import UserPublic, UserJWT, UserInUpdateEmail, UserInUpdatePassword, UserBio, \
    UserInternal, UserInUpdateUsername
from ..dependencies.dao import get_dao

from ..dao.users import UserDao
from ..errors import EntityDoesNotExist
from ..dependencies.security import verify_token, verify_token_internal

from .. import strings


router = APIRouter()


@router.get("/{user_id}", name="users:read-user", status_code=200, response_model=UserPublic)
async def read_user(
    user_id: int,
    userJwt: UserJWT = Depends(verify_token),
    userDao: UserDao = Depends(get_dao(UserDao))
) -> UserPublic:
    try:
        return await userDao.read(user_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.USER_ERROR01.format(user_id)
        )


@router.patch("/email", name="users:update-email", status_code=200)
async def update_user_email(
    userInUpdateEmail: UserInUpdateEmail,
    userInternal: UserInternal = Depends(verify_token_internal),
    userDao: UserDao = Depends(get_dao(UserDao))
) -> None:

    if not userInternal.check_password(userInUpdateEmail.user.password):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.USER_ERROR02
        )

    elif (userInternal.check_email(userInUpdateEmail.user.email) or
          userInternal.check_username(userInUpdateEmail.user.user_name)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.USER_ERROR04
        )
    try:
        await userDao.get_user_by_email(email=userInUpdateEmail.email)
    except EntityDoesNotExist:
        pass
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USER_ERROR06
        )
    await userDao.update_email(user_id=userInternal.user_id, email=userInUpdateEmail.email)
    await userDao.invalidate_previous_token(user=userInternal)


@router.patch("/username", name="users:update-username", status_code=200)
async def update_user_name(
    userInUpdateUsername: UserInUpdateUsername,
    userInternal: UserInternal = Depends(verify_token_internal),
    userDao: UserDao = Depends(get_dao(UserDao))
) -> None:
    if not userInternal.check_password(userInUpdateUsername.user.password):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.USER_ERROR02
        )
    elif (userInternal.check_email(userInUpdateUsername.user.email) or
          userInternal.check_username(userInUpdateUsername.user.user_name)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.USER_ERROR04
        )
    try:
        await userDao.get_user_by_username(user_name=userInUpdateUsername.user_name)
    except EntityDoesNotExist:
        pass
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USER_ERROR05
        )
    await userDao.update_user_name(user_id=userInternal.user_id, user_name=userInUpdateUsername.user_name)
    await userDao.invalidate_previous_token(user=userInternal)


@router.patch("/password", name="users:update-password", status_code=200)
async def update_user_password(
    userInUpdatePassword: UserInUpdatePassword,
    userInternal: UserInternal = Depends(verify_token_internal),
    userDao: UserDao = Depends(get_dao(UserDao))
) -> None:

    if not userInternal.check_password(userInUpdatePassword.user.password):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.USER_ERROR02
        )
    elif (userInternal.check_email(userInUpdatePassword.user.email) or
          userInternal.check_username(userInUpdatePassword.user.user_name)):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.USER_ERROR04
        )
    await userDao.update_password(user=userInternal, password=userInUpdatePassword.password)


@router.patch("/bio", name="users:update-bio", status_code=200)
async def update_user_bio(
    userBio: UserBio,
    userJwt: UserJWT = Depends(verify_token),
    userDao: UserDao = Depends(get_dao(UserDao))
) -> None:
    await userDao.update_bio(user_id=userJwt.user_id, bio=userBio.bio)
