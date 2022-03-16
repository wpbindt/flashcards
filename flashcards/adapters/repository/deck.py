from abc import ABC, abstractmethod
from typing import Optional, AbstractSet
from uuid import UUID

from flashcards.adapters.dto.deck import DeckDTO
from flashcards.adapters.dto.mappers import deck_from_dto
from flashcards.adapters.key_value_store.key_value_store import KeyValueStore
from flashcards.adapters.key_value_store.query import FieldEqual, FieldContains
from flashcards.domain.deck import DeckId, Deck
from flashcards.domain.flashcard import FlashcardId


class DeckRepository(ABC):
    @abstractmethod
    def add(self, deck: Deck) -> None:
        ...

    @abstractmethod
    def get(self, deck_id: DeckId) -> Deck:
        ...

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Deck]:
        ...

    @abstractmethod
    def find_by_flashcard(self, flashcard_id: FlashcardId) -> AbstractSet[Deck]:
        ...


class DeckNotFound(Exception):
    ...


class KeyValueDeckRepository(DeckRepository):
    def __init__(
        self,
        store: KeyValueStore[UUID, DeckDTO],
    ):
        self._store = store

    def get(self, deck_id: DeckId) -> Deck:
        dto = self._store.get(key=deck_id)
        return deck_from_dto(dto)

    def add(self, deck: Deck) -> None:
        dto = DeckDTO.from_domain_object(deck)
        self._store.set(dto.id, dto)

    def find_by_name(self, name: str) -> Optional[Deck]:
        matches = self._store.find(FieldEqual(field='name', value=name))
        if len(matches) == 0:
            return None
        return deck_from_dto(matches[0])

    def find_by_flashcard(self, flashcard_id: FlashcardId) -> AbstractSet[Deck]:
        matches = self._store.find(FieldContains(field='cards', value=flashcard_id))
        return set(map(deck_from_dto, matches))
