from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

TMessage = TypeVar("TMessage")
TResult = TypeVar("TResult")


@dataclass
class BaseCommand:
    pass


@dataclass
class BaseQuery:
    pass


class CommandHandler(ABC, Generic[TMessage, TResult]):
    @abstractmethod
    async def handle(self, command: TMessage) -> TResult:
        pass


class QueryHandler(ABC, Generic[TMessage, TResult]):
    @abstractmethod
    async def handle(self, query: TMessage) -> TResult:
        pass
