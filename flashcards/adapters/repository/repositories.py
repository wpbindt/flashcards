from dataclasses import dataclass

from flashcards.adapters.dto.deck import DeckDTO
from flashcards.adapters.dto.flashcard import FlashcardDTO
from flashcards.adapters.key_value_store.postgres import PGKeyValueStore
from flashcards.adapters.key_value_store.fake import FakeKeyValueStore
from flashcards.adapters.repository.deck import DeckRepository, KeyValueDeckRepository
from flashcards.adapters.transaction.fake_transaction import FakeTransaction
from flashcards.adapters.transaction.pg_transaction import PGTransaction
from flashcards.adapters.repository.flashcard import FlashcardRepository, KeyValueFlashcardRepository


@dataclass
class Repositories:
    flashcard: FlashcardRepository
    deck: DeckRepository


def pg_repositories_factory(transaction: PGTransaction) -> Repositories:
    return Repositories(
        flashcard=KeyValueFlashcardRepository(
            store=PGKeyValueStore(
                transaction=transaction,
                table_name='flashcards',
                dump_key=str,
                dump_value=lambda dto: dto.json(),
                restore_value=lambda raw_data: FlashcardDTO(**raw_data),
            )
        ),
        deck=KeyValueDeckRepository(
            store=PGKeyValueStore(
                transaction=transaction,
                table_name='decks',
                dump_key=str,
                dump_value=lambda dto: dto.json(),
                restore_value=lambda raw_data: DeckDTO(**raw_data),
            )
        ),
    )


def fake_repositories_factory(transaction: FakeTransaction) -> Repositories:
    return Repositories(
        flashcard=KeyValueFlashcardRepository(
            store=FakeKeyValueStore(
                values={},
                dump_value=lambda dto: dto.dict(),
            )
        ),
        deck=KeyValueDeckRepository(
            store=FakeKeyValueStore(
                values={},
                dump_value=lambda dto: dto.dict(),
            )
        ),
    )
