class AppBaseException(Exception):

    def __init__(
        self, message: str, status_code: int, errors: list[str] | None = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        super().__init__(self.message)
