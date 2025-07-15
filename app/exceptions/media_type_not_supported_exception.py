from .base_exception import AppBaseException


class MediaTypeNotSupportedException(AppBaseException):
    def __init__(self, message: str = "Media type not supported") -> None:
        super().__init__(message, status_code=415)
