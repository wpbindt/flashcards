from __future__ import annotations
from abc import ABC, abstractmethod


class Transaction(ABC):
    @abstractmethod
    def __enter__(self) -> Transaction:
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        ...

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...
