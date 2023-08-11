from .common import UnauthorizedException
from .error_type import ErrorType


class InvalidTokenException(UnauthorizedException):
    def __init__(self, errorType: ErrorType) -> None:
        super().__init__(errorType)
