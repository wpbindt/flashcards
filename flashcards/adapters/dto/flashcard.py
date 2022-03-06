from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from flashcards.domain.flashcard import Flashcard


class FlashcardDTO(BaseModel):
    front: str
    back: str
    id: UUID

    class Config:
        allow_mutation = False
        frozen = True

    @classmethod
    def from_domain_object(cls, domain_object: Flashcard) -> FlashcardDTO:
        return cls(
            id=domain_object.id,
            front=domain_object.front,
            back=domain_object.back,
        )
