# pyright: basic
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from uuid import UUID

from pydantic import BaseModel

from app.infrastructure.database import DatabaseSessionManager


T = TypeVar("T")
C = TypeVar("C", bound=BaseModel)
U = TypeVar("U")


class Repository(ABC, Generic[T, C, U]):
    def __init__(self):
        self.db = DatabaseSessionManager().get_session()

    @property
    @abstractmethod
    def model(self) -> type[T]:
        pass

    def find_by_id(self, id: int | UUID) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def find_by_ids(self, ids: List[UUID] | List[int]) -> List[T]:
        return self.db.query(self.model).filter(self.model.id.in_(ids)).all()

    def find_all(
        self,
    ) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, data: C, extra_attrs: dict | None = None) -> T:
        data_dict = data.model_dump()

        if extra_attrs:
            data_dict.update(extra_attrs)

        obj = self.model(**data_dict)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, model: T) -> T:
        self.db.delete(model)
        self.db.commit()

        return model

    def update(self, data: U, model: T) -> T:
        data_dict = data.model_dump(exclude_unset=True)

        for key, value in data_dict.items():
            setattr(model, key, value)

        self.db.commit()
        self.db.refresh(model)
        return model
