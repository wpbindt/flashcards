from flashcards.adapters.transaction.transaction import Transaction


class FakeTransaction(Transaction):
    def __enter__(self) -> Transaction:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):  # type: ignore
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
