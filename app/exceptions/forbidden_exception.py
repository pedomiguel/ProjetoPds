from .base_exception import AppBaseException


class ForbiddenException(AppBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=403)
