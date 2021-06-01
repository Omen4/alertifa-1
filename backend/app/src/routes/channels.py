from fastapi import APIRouter, Body, Depends, Path, HTTPException, Header
from starlette import status

from ..models.channels import ChannelInResponse
from ..models.users import UserInDB
from ..dependencies.dao import get_dao
from ..dao.channels import ChannelDao
from ..errors import EntityDoesNotExist
# from ..config import SECRET_KEY
from ..dependencies.security import verify_token
from ..strings import CHANNEL_ERROR01

from starlette.requests import Request


router = APIRouter()


@router.get(
    "/{channel_id}", 
    response_model=ChannelInResponse,
    name="channels:get-channel-by-id"
)
async def list_channels(
    channel_id: int,
    channelDao: ChannelDao = Depends(get_dao(ChannelDao)),
    user: UserInDB = Depends(verify_token)
) -> ChannelInResponse:
    try:
        channel = await channelDao.get_channel_by_id(channel_id=channel_id)
        return ChannelInResponse(channel=channel)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CHANNEL_ERROR01.format(channel_id)
        )