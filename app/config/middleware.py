from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.exception_handler import ExceptionHandler
from app.middlewares.database_session import DBSessionMiddleware

class MiddlewareManager:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def setup(self):
        self._add_cors()
        self._add_exception_handler()
        self._add_db_session_middleware()

    def _add_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _add_exception_handler(self):
        ExceptionHandler(self.app)

    def _add_db_session_middleware(self):
        self.app.add_middleware(DBSessionMiddleware)
