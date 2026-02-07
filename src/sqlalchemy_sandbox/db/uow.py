from contextlib import AbstractContextManager
from types import TracebackType
from sqlalchemy_sandbox.db.db import sessions
from sqlalchemy.orm import Session

from typing import Any, TypeVar, Type

T = TypeVar("T", bound=Any)


class SqlRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, obj: Any) -> None:
        self.session.add(obj)

    def load_all(self, model: Type[T]) -> list[T]:
        objs = self.session.query(model).all()
        return objs

    def cancel(self) -> None:
        self.session.rollback()

    def commit(self) -> None:
        self.session.commit()


class SqlUnitOfWork(AbstractContextManager):
    def __init__(self, db_name: str = "default") -> None:
        self.repo = SqlRepository(sessions[db_name]())

    def __enter__(self) -> SqlRepository:
        return self.repo

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_value:
            self.repo.cancel()
        self.repo.commit()
