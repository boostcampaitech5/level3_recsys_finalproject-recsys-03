from .error_type import ErrorType


class BadRequestException(Exception):
    def __init__(self, errorType: ErrorType) -> None:
        super().__init__(errorType.message)
        self.code = errorType.code


class UnauthorizedException(Exception):
    def __init__(self, errorType: ErrorType) -> None:
        super().__init__(errorType.message)
        self.code = errorType.code
