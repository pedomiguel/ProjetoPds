from .base_exception import AppBaseException


class UnauthorizedException(AppBaseException):

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, status_code=401)
