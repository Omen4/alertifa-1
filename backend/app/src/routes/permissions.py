from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..models.permissions import Permission
from ..models.users import UserInDB, UserJWT
from ..dependencies.dao import get_dao
from ..dao.channels import ChannelDao
from ..dao.users import UserDao
from ..dao.permissions import PermissionDao
from ..dao.roles import RoleDao
from ..errors import EntityDoesNotExist
from ..dependencies.security import verify_token
from .. import strings


router = APIRouter()


@router.get("/me", response_model=List[Permission], name="permissions:get-user-permissions")
async def list_permissions(
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao))
) -> List[Permission]:
    try:
        permissions: List[Permission] = await permissionDao.get_user_permissions_from_id(user_id=user.user_id)
        return permissions
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.PERMISSION_ERROR01
        )


@router.patch("/modify", name="permissions:change-permission")
async def change_permission(
    permission: Permission,
    user: UserJWT = Depends(verify_token),
    userDao: UserDao = Depends(get_dao(UserDao)),
    channelDao: ChannelDao = Depends(get_dao(ChannelDao)),
    roleDao: RoleDao = Depends(get_dao(RoleDao)),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao))
) -> None:
    try:
        await userDao.read(user_id=permission.user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.USER_ERROR01.format(permission.user_id)
        )
    try:
        await channelDao.get_channel_by_id(channel_id=permission.channel_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.CHANNEL_ERROR01.format(permission.channel_id)
        )
    try:
        await roleDao.find_by_id(role_id=permission.role_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.ROLE_ERROR01.format(permission.role_id)
        )
    try:
        mod_privileges: int = await permissionDao.get_user_permission(user_id=user.user_id, channel_id=permission.channel_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
    user_privileges: int
    try:
        user_privileges = await permissionDao.get_user_permission(user_id=permission.user_id, channel_id=permission.channel_id)
    except EntityDoesNotExist:
        await permissionDao.create_permission(user_id=permission.user_id, channel_id=permission.channel_id)
        user_privileges = 0

    if (mod_privileges >= 3 and user_privileges < 3) and (permission.role_id < 3):
        await permissionDao.set_permission(user_id=permission.user_id, channel_id=permission.channel_id, role_id=permission.role_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
