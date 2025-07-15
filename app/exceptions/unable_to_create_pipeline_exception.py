from .base_exception import AppBaseException


class UnableToCreatePipelineException(AppBaseException):
    def __init__(self, message: str = "Unable to create pipeline") -> None:
        super().__init__(message, status_code=500)
