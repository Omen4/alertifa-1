from fastapi import APIRouter, Body, Depends, Path, HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from ..models.users import UserInDB, UserJWT
from ..models.messages import MessageInRequest, MessageInResponse
from ..dependencies.dao import get_dao
from ..dao.permissions import PermissionDao
from ..dao.channels import ChannelDao
from ..dao.roles import RoleDao


from ..dao.messages import MessageDao
from ..errors import EntityDoesNotExist
from ..dependencies.security import verify_token, check_permission

from .. import strings


router = APIRouter()


@router.post("/me/{channel_id}", name="messages:post-on-channel", status_code=201)
async def create_message(
    message: MessageInRequest,
    channel_id: int = Path(..., ge=1),
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao)),
    messageDao: MessageDao = Depends(get_dao(MessageDao)),
    channelDao: ChannelDao = Depends(get_dao(ChannelDao)),
    roleDao: RoleDao = Depends(get_dao(RoleDao))
) -> None:

    try:
        await channelDao.get_channel_by_id(channel_id=channel_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.CHANNEL_ERROR01.format(channel_id)
        )
    try:
        await permissionDao.check_permission(user_id=user.user_id, channel_id=channel_id, minimum_role=2)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
    await messageDao.create(channel_id=channel_id, user_id=user.user_id, body=message.body)


@router.patch("/me/{message_id}", name="messages:edit-my-message", status_code=200)
async def edit_message(
    message_id: int,
    message: MessageInRequest,
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao)),
    messageDao: MessageDao = Depends(get_dao(MessageDao)),
    channelDao: ChannelDao = Depends(get_dao(ChannelDao))
) -> None:

    try:
        await permissionDao.check_user_is_owner(user_id=user.user_id, message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
    await messageDao.update(message_id=message_id, body=message.body)


@router.delete("/me/{message_id}", name="messages:delete-my-message", status_code=200)
async def delete_message(
    message_id: int,
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao)),
    messageDao: MessageDao = Depends(get_dao(MessageDao)),
    channelDao: ChannelDao = Depends(get_dao(ChannelDao))
) -> None:

    try:
        await permissionDao.check_user_is_owner(user_id=user.user_id, message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
    await messageDao.delete(message_id=message_id)


@router.get("/{message_id}", name="messages:read-message", status_code=200)
async def read_message(
    message_id: int,
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao)),
    messageDao: MessageDao = Depends(get_dao(MessageDao)),
    channelDao: ChannelDao = Depends(get_dao(ChannelDao))
) -> MessageInResponse:

    try:
        await permissionDao.check_permission_from_message_id(user_id=user.user_id, message_id=message_id, role_id=1)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
    try:
        return await messageDao.read(message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.MESSAGE_ERROR01
        )


@router.patch("/{message_id}", name="messages:edit-message-mod", status_code=200)
async def edit_message_mod(
    message_id: int,
    message: MessageInRequest,
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao)),
    messageDao: MessageDao = Depends(get_dao(MessageDao))
) -> None:

    try:
        await messageDao.read(message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.MESSAGE_ERROR01
        )
    try:
        await permissionDao.check_mod_privileges(user_id=user.user_id, message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
    await messageDao.update(message_id=message_id, body=message.body)


@router.delete("/{message_id}", name="messages:delete-message-mod", status_code=200)
async def delete_message_mod(
    message_id: int,
    user: UserJWT = Depends(verify_token),
    permissionDao: PermissionDao = Depends(get_dao(PermissionDao)),
    messageDao: MessageDao = Depends(get_dao(MessageDao))
) -> None:

    try:
        await messageDao.read(message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.MESSAGE_ERROR01
        )
    try:
        await permissionDao.check_mod_privileges(user_id=user.user_id, message_id=message_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=strings.PERMISSION_ERROR02
        )
