from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError

from app.exceptions import AppBaseException
from app.config import Logger


class ExceptionHandler:

    def __init__(self, app):
        self.app = app
        self.register_handlers()

    def register_handlers(self):
        self.app.add_exception_handler(
            AppBaseException, self.app_base_exception_handler
        )
        self.app.add_exception_handler(
            RequestValidationError, self.validation_exception_handler
        )
        self.app.add_exception_handler(Exception, self.generic_exception_handler)

    async def app_base_exception_handler(self, _: Request, exc: AppBaseException):
        error_response = {"message": exc.message}
        if exc.errors:
            error_response["errors"] = exc.errors

        return JSONResponse(status_code=exc.status_code, content=error_response)

    async def validation_exception_handler(
        self, _: Request, exc: RequestValidationError
    ):
        errors = {}
        for err in exc.errors():
            loc = [str(l) for l in err["loc"] if l != "body"]
            field = ".".join(loc)
            msg = err["msg"]
            errors[field] = msg

        return JSONResponse(
            status_code=422,
            content={"message": "Validation Error", "errors": errors},
        )

    async def generic_exception_handler(self, request: Request, exc: Exception):
        Logger.error(f"{request.method} {request.url.path}", str(exc))
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
