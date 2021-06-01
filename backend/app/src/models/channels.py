from pydantic import BaseConfig, BaseModel, Field, validator
from .base import Base, BaseBis


class Channel(BaseBis):
    channel_id: int
    channel_name: str

class ChannelInResponse(BaseModel):
    channel: Channel
