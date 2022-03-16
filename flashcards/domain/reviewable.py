from datetime import datetime, timedelta
from math import floor
from typing import Any, NewType
from uuid import UUID

from flashcards.domain.entity import Entity

ReviewableId = NewType('ReviewableId', UUID)


class Reviewable(Entity[ReviewableId]):
    REVIEW_INTERVAL_EXPONENT = 1.49

    def __init__(
        self,
        reviewable_id: ReviewableId,
        question: str,
        answer: str,
        review_at: datetime,
        correct_answers: int = 0,
    ) -> None:
        self._reviewable_id = reviewable_id
        self.question = question
        self.answer = answer
        self.correct_answers = correct_answers
        self.review_at = review_at

    @property
    def id(self) -> ReviewableId:
        return self._reviewable_id

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Reviewable):
            # compare on ids to make ordering total
            return (self.review_at, self.id) < (other.review_at, other.id)
        raise TypeError

    def mark_incorrect(self) -> None:
        self.correct_answers = 0
        self._reschedule()

    def mark_correct(self) -> None:
        self.correct_answers += 1
        self._reschedule()

    def reset(self) -> None:
        self.mark_incorrect()

    def _reschedule(self) -> None:
        self.review_at = (
            datetime.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            + timedelta(days=floor(self.REVIEW_INTERVAL_EXPONENT ** self.correct_answers) - 1)
        )
