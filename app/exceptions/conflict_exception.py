from .base_exception import AppBaseException


class ConflictException(AppBaseException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)
