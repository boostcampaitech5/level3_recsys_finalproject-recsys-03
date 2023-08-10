import jwt
from datetime import datetime
from ..exceptions.auth import InvalidTokenException
from ..exceptions.error_type import ErrorType


def encode_jwt(payload: dict[str], exp: datetime, secret: str) -> str:
    return jwt.encode({**payload, "exp": exp}, secret, algorithm="HS256")


def decode_jwt(token: str, secret: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException(ErrorType.EXPIRED_TOKEN)
    except jwt.InvalidTokenError:
        raise InvalidTokenException(ErrorType.INVALID_TOKEN)
