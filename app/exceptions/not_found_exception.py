from .base_exception import AppBaseException


class NotFoundException(AppBaseException):

    def __init__(self, message: str, errors: list[str] | None = None) -> None:
        super().__init__(message, status_code=404, errors=errors)
