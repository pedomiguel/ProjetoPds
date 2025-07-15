import inspect
import sys
from app.controllers import BaseController
from fastapi import FastAPI


class Router:
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    def register(self):
        for name, obj in inspect.getmembers(sys.modules["app.controllers"]):
            if inspect.isclass(obj) and issubclass(obj, BaseController):
                if not inspect.isabstract(obj):
                    instance = obj()
                    self.app.include_router(instance.router)
