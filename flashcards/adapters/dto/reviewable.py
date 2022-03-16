from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel

from flashcards.domain.reviewable import Reviewable


class ReviewableDTO(BaseModel):
    id: UUID
    question: str
    answer: str
    correct_answers: int
    review_after: datetime.datetime

    class Config:
        frozen = True
        allow_mutation = False

    @classmethod
    def from_domain_object(cls, domain_object: Reviewable) -> ReviewableDTO:
        return cls(
            id=domain_object.id,
            question=domain_object.question,
            answer=domain_object.answer,
            review_after=domain_object.review_at,
            correct_answers=domain_object.correct_answers,
        )
