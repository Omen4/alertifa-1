from typing import Dict, TypeVar, Union, Any
import datetime
import jwt

from fastapi import Header
from ..config import SECRET_KEY, ALGORITHM, AUTH_HEADER, AUTH_SCHEME, TOKEN_VALIDITY
from ..models.users import UserJWT, UserWithToken
import src.strings as strings

T = TypeVar('T', bound='JWTUtil')


class JWTUtil(object):
    secret_key: str = str(SECRET_KEY)
    algorithm: str = ALGORITHM
    auth_header: str = AUTH_HEADER
    auth_scheme: str = AUTH_SCHEME
    token_validity: int = TOKEN_VALIDITY

    def __init__(self, token: str) -> None:
        self.token: str = token

    @classmethod
    def from_header(cls, headers: Header) -> T:
        auth_header = headers.get(cls.auth_header)
        if auth_header is None:
            raise Exception(strings.AUTH_ERROR01)
        if auth_header[:7] != (cls.auth_scheme + " "):
            raise Exception(strings.AUTH_ERROR02)
        return cls(auth_header[7:])

    @classmethod
    def from_user(cls, user: UserJWT) -> T:
        expires_delta = datetime.timedelta(minutes=cls.token_validity)
        expires_at: datetime.datetime = datetime.datetime.utcnow() + expires_delta
        jwt_content: Dict[str, Any] = {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "jwt_id": user.jwt_id,
            "expires_at": expires_at.isoformat()
        }
        token: str = jwt.encode(jwt_content, cls.secret_key, algorithm=cls.algorithm)
        return cls(token)

    def check(self) -> None:
        try:
            decoded: Dict[str, str] = jwt.decode(
                self.token,
                str(self.secret_key),
                algorithms=[self.algorithm]
            )
        except jwt.exceptions.InvalidSignatureError:
            raise Exception(strings.TOKEN_ERROR01)
        except Exception:
            raise Exception(strings.TOKEN_ERROR02)

        try:
            expires_at: datetime.datetime = datetime.datetime.fromisoformat(decoded.get('expires_at'))
            delta: datetime.timedelta = expires_at - datetime.datetime.utcnow()
        except Exception:
            raise Exception(strings.TOKEN_ERROR02)
        if delta.total_seconds() < 0:
            raise Exception(strings.TOKEN_ERROR03)

    def get_user(self) -> UserJWT:
        decoded: Dict[str, str] = jwt.decode(
            self.token,
            str(self.secret_key),
            algorithms=[self.algorithm]
        )
        return UserJWT(
            user_id=decoded.get('user_id'),
            user_name=decoded.get('user_name'),
            email=decoded.get('email'),
            jwt_id=decoded.get('jwt_id'),
            expires_at=datetime.datetime.fromisoformat(decoded.get('expires_at'))
        )

    def get_user_with_token(self) -> UserWithToken:
        decoded: Dict[str, str] = jwt.decode(
            self.token,
            str(self.secret_key),
            algorithms=[self.algorithm]
        )
        return UserWithToken(
            user=UserJWT(
                user_id=decoded.get('user_id'),
                user_name=decoded.get('user_name'),
                email=decoded.get('email'),
                jwt_id=decoded.get('jwt_id'),
                expires_at=datetime.datetime.fromisoformat(decoded.get('expires_at'))
            ),
            token=self.token
        )
