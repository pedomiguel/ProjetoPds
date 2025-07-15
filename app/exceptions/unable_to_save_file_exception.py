from .base_exception import AppBaseException


class UnableToSaveFileException(AppBaseException):

    def __init__(self, message: str = "Unable to save file") -> None:
        super().__init__(message, status_code=500)
