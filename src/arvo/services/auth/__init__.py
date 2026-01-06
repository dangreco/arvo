import jwt
from datetime import datetime, timedelta, timezone
from enum import Enum

from arvo.config import config


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    def delta(self) -> timedelta:
        if self == TokenType.ACCESS:
            return timedelta(minutes=15)
        elif self == TokenType.REFRESH:
            return timedelta(days=7)
        else:
            raise ValueError("Invalid token type")


class AuthService:
    @staticmethod
    def create_token(user_id: int, type_: TokenType) -> str:
        payload = {
            "sub": str(user_id),
            "type": type_.value,
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + type_.delta(),
        }
        token = jwt.encode(payload, config.jwt.secret, algorithm=config.jwt.algorithm)
        return token

    @staticmethod
    def verify_token(token: str, type_: TokenType) -> dict:
        try:
            payload = jwt.decode(
                token, config.jwt.secret, algorithms=[config.jwt.algorithm]
            )
            if payload.get("type") != type_.value:
                raise jwt.InvalidTokenError("invalid token type")
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("token has expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("invalid token")
