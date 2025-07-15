from abc import ABC, abstractmethod

from fastapi import APIRouter


class BaseController(ABC):
    def __init__(self, tags: list = [], prefix: str = "") -> None:
        self._router = APIRouter(tags=tags, prefix=prefix)
        self.add_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    @abstractmethod
    def add_routes(self) -> None: ...
