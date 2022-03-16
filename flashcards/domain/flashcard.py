from typing import NewType
from uuid import UUID

from flashcards.domain.entity import Entity

FlashcardId = NewType('FlashcardId', UUID)


class Flashcard(Entity[FlashcardId]):
    def __init__(
        self,
        flashcard_id: FlashcardId,
        front: str,
        back: str,
    ) -> None:
        self._flashcard_id = flashcard_id
        self.front = front
        self.back = back

    @property
    def id(self) -> FlashcardId:
        return self._flashcard_id
