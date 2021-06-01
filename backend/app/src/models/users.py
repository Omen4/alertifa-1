from typing import Optional
import datetime

from pydantic import BaseConfig, BaseModel, Field, validator, EmailStr, HttpUrl

from ..utils.security import generate_salt, verify_password, get_password_hash
from .base import Base


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


class BaseTest(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}


class User(Base):
    # user_name: str
    email: str
    password: str


class UserJWT(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr
    jwt_id: int


class UserWithToken(BaseModel):
    user: UserJWT
    token: str


class UserInternal(UserJWT):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)

    def check_email(self, email: str) -> bool:
        return self.email != email

    def check_username(self, user_name: str) -> bool:
        return self.user_name != user_name


class UserInDB(BaseModel):
    user_name: str
    email: str
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(BaseModel):
    user_name: str
    password: str
    email: EmailStr

    @validator('user_name')
    def check_username(cls, v) -> str:
        if len(v) < 3 or len(v) > 20:
            raise ValueError('user name should be between 3 and 20 ASCII characters')
        return v

    @validator('password')
    def check_password(cls, v) -> str:
        if len(v) < 8:
            raise ValueError('Password should be 8 characters long')
        return v

    @validator('email')
    def check_email(cls, v) -> str:
        if len(v) < 4:
            raise ValueError('Invalid email')
        return v


class UserInUpdate(BaseModel):
    user: UserInCreate
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInUpdateEmail(BaseModel):
    user: UserInCreate
    email: EmailStr


class UserInUpdateUsername(BaseModel):
    user: UserInCreate
    user_name: str


class UserInUpdatePassword(BaseModel):
    user: UserInCreate
    password: str


class UserName(BaseModel):
    user_name: str


class UserInResponse(BaseModel):
    user: UserWithToken


class UserInMessage(BaseModel):
    user_id: int
    user_name: str


class UserPublic(BaseModel):
    user_id: int
    user_name: str
    created_at: datetime.datetime 
    email: Optional[EmailStr]
    bio: Optional[str]


class UserBio(BaseModel):
    bio: str
