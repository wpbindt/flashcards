from __future__ import annotations
from typing import Optional

import psycopg2
from psycopg2.extensions import connection, cursor

from flashcards.config import PostgresConfig
from flashcards.adapters.transaction.transaction import Transaction


class PGTransaction(Transaction):
    def __init__(self, database_uri: str) -> None:
        self._config = PostgresConfig.from_uri(database_uri)
        self._connection: Optional[connection] = None
        self._transaction_began = False
        self._committed = False

    def __enter__(self) -> PGTransaction:
        self._transaction_began = True
        self._connection = psycopg2.connect(self._config.to_dsn())
        self.cursor: cursor = self._connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        self._connection.close()

    def commit(self) -> None:
        if self._connection is None:
            raise ValueError
        self._connection.commit()
        self._committed = True

    def rollback(self) -> None:
        if self._connection is None:
            raise ValueError
        if not self._committed:
            self._connection.rollback()
