from __future__ import annotations
from typing import Tuple
from uuid import UUID

from pydantic import BaseModel

from flashcards.adapters.dto.reviewable import ReviewableDTO
from flashcards.domain.flashcard import Deck


class DeckDTO(BaseModel):
    id: UUID
    name: str
    cards: Tuple[Tuple[UUID, Tuple[ReviewableDTO, ...]], ...]

    class Config:
        allow_mutation = False
        frozen = True

    @classmethod
    def from_domain_object(cls, domain_object: Deck) -> DeckDTO:
        return cls(
            id=domain_object.id,
            cards=tuple(
                (flashcard_id, tuple(ReviewableDTO.from_domain_object(reviewable) for reviewable in reviewables))
                for flashcard_id, reviewables in domain_object.cards.items()
            ),
            name=domain_object.name,
        )
