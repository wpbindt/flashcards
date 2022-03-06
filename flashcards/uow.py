from __future__ import annotations
from typing import Callable, TypeVar, Generic

from flashcards.adapters.repository.repositories import Repositories
from flashcards.adapters.transaction.transaction import Transaction


TransactionType = TypeVar('TransactionType', bound=Transaction)


class UnitOfWork(Generic[TransactionType]):
    def __init__(
        self,
        transaction: TransactionType,
        repo_factory: Callable[[TransactionType], Repositories]
    ):
        self._transaction = transaction
        self.repositories = repo_factory(transaction)

    def __enter__(self) -> None:
        self._transaction.__enter__()

    def __exit__(self, *excs):  # type: ignore
        self._transaction.__exit__(*excs)

    def commit(self) -> None:
        self._transaction.commit()

    def rollback(self) -> None:
        self._transaction.rollback()
