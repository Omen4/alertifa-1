from typing import List, Optional
import datetime

from pydantic import BaseConfig, BaseModel, Field, validator

from .channels import Channel
from .users import User, UserInMessage


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")

def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )

class Message(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        alias_generator = convert_field_to_camel_case

    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        return value or datetime.datetime.now()


class MessageInRequest(BaseModel):
    body: str


class MessageInResponse(BaseModel):
    user: UserInMessage
    channel: Channel
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
    body: str

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        return value or datetime.datetime.now()
