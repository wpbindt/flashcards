from collections import defaultdict
from datetime import datetime
from typing import NewType, Optional, Dict, Set, List
from uuid import UUID, uuid4

from flashcards.domain.entity import Entity
from flashcards.domain.flashcard import FlashcardId, Flashcard
from flashcards.domain.reviewable import Reviewable, ReviewableId

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

    def remove_flashcard(self, flashcard_id: FlashcardId) -> None:
        self.cards.pop(flashcard_id, None)

    @property
    def id(self) -> DeckId:
        return self._deck_id
