from abc import ABC, abstractmethod
from uuid import UUID

from flashcards.adapters.dto.flashcard import FlashcardDTO
from flashcards.adapters.dto.mappers import flashcard_from_dto
from flashcards.adapters.key_value_store.key_value_store import KeyValueStore
from flashcards.domain.flashcard import Flashcard, FlashcardId


class FlashcardRepository(ABC):
    @abstractmethod
    def add(self, flashcard: Flashcard) -> None:
        ...

    @abstractmethod
    def get(self, flashcard_id: FlashcardId) -> Flashcard:
        ...


class FlashcardNotFound(Exception):
    ...


class KeyValueFlashcardRepository(FlashcardRepository):
    def __init__(
        self,
        store: KeyValueStore[UUID, FlashcardDTO],
    ):
        self._store = store

    def get(self, flashcard_id: FlashcardId) -> Flashcard:
        dto = self._store.get(key=flashcard_id)
        return flashcard_from_dto(dto)

    def add(self, flashcard: Flashcard) -> None:
        dto = FlashcardDTO.from_domain_object(flashcard)
        self._store.set(dto.id, dto)
