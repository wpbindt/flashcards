from collections import defaultdict
from datetime import datetime, timedelta
from math import floor
from typing import NewType, Any, Dict, Set, List, Optional
from uuid import UUID, uuid4

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
        return False

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


DeckId = NewType('DeckId', UUID)


class Deck(Entity[DeckId]):
    def __init__(
        self,
        deck_id: DeckId,
        name: str,
        cards: Optional[Dict[FlashcardId, Set[Reviewable]]] = None,
    ) -> None:
        self._deck_id = deck_id
        self.name = name
        if cards is None:
            cards = defaultdict(set)
        self.cards = cards

    def cards_to_review(self, datetime: datetime) -> List[Reviewable]:
        reviewables_for_datetime = {
            reviewable
            for reviewable in self._all_reviewables
            if reviewable.review_at < datetime
        }
        return sorted(reviewables_for_datetime)

    def add_card(self, flashcard: Flashcard, both_sides: bool = False) -> None:
        if flashcard.id in self.cards:
            raise Exception
        review_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.cards[flashcard.id].add(Reviewable(
            reviewable_id=ReviewableId(uuid4()),
            answer=flashcard.back,
            question=flashcard.front,
            review_at=review_time,
        ))
        if both_sides:
            self.cards[flashcard.id].add(Reviewable(
                reviewable_id=ReviewableId(uuid4()),
                answer=flashcard.front,
                question=flashcard.back,
                review_at=review_time,
            ))

    @property
    def _all_reviewables(self) -> Set[Reviewable]:
        return set().union(*self.cards.values())

    def mark_correct(self, reviewable_ids: Set[ReviewableId]) -> None:
        for reviewable in self._all_reviewables:
            if reviewable.id not in reviewable_ids:
                continue
            reviewable.mark_correct()

    def mark_incorrect(self, reviewable_ids: Set[ReviewableId]) -> None:
        for reviewable in self._all_reviewables:
            if reviewable.id not in reviewable_ids:
                continue
            reviewable.mark_incorrect()

    def reset(self, reviewable_ids: Set[ReviewableId]) -> None:
        for reviewable in self._all_reviewables:
            if reviewable.id not in reviewable_ids:
                continue
            reviewable.reset()

    def reset_all(self) -> None:
        for reviewable in self._all_reviewables:
            reviewable.reset()

    @property
    def id(self) -> DeckId:
        return self._deck_id
