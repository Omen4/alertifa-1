from pydantic import BaseModel


class Permission(BaseModel):
    channel_id: int
    role_id: int
    user_id: int
