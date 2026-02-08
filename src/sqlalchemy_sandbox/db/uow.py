from contextlib import AbstractContextManager
from types import TracebackType
from sqlalchemy_sandbox.db.db import session_makers
from sqlalchemy.orm import Session, sessionmaker
import uuid
from typing import Any, TypeVar, Type

T = TypeVar("T", bound=Any)


class SqlRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, obj: T) -> T:
        self.session.add(obj)
        return obj

    def load_all(self, model: Type[T]) -> list[T]:
        objs = self.session.query(model).all()
        return objs

    def get_by_id(self, model: Type[T], id: uuid.UUID) -> T | None:
        return self.session.query(model).get(id)

    def delete(self, obj: Any) -> None:
        self.session.delete(obj)


class SqlUnitOfWork(AbstractContextManager):
    def __init__(
        self,
        db_name: str = "default",
        session_factory: dict[str, sessionmaker[Session]] | None = None,
    ) -> None:
        if not session_factory:
            session_factory = session_makers
        self.session_factory = session_factory[db_name]

    def __enter__(self) -> SqlRepository:
        self.session = self.session_factory()
        self.repo = SqlRepository(self.session)
        return self.repo

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        try:
            if exc_value:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()
