import os

from flashcards.adapters.repository.repositories import pg_repositories_factory, \
    fake_repositories_factory
from flashcards.adapters.transaction.fake_transaction import FakeTransaction
from flashcards.adapters.transaction.pg_transaction import PGTransaction
from flashcards.uow import UnitOfWork


def get_pg_uow() -> UnitOfWork:
    return UnitOfWork(
        repo_factory=pg_repositories_factory,
        transaction=get_pg_transaction(),
    )


def get_fake_uow() -> UnitOfWork:
    return UnitOfWork(
        repo_factory=fake_repositories_factory,
        transaction=FakeTransaction(),
    )


def get_pg_transaction() -> PGTransaction:
    return PGTransaction(database_uri=os.environ.get('DATABASE_URI', ''))


def get_api_url() -> str:
    return os.environ['API_URL']
