from collections import defaultdict

from flashcards.adapters.dto.flashcard import FlashcardDTO
from flashcards.adapters.dto.deck import DeckDTO
from flashcards.adapters.dto.reviewable import ReviewableDTO
from flashcards.domain.flashcard import Flashcard, FlashcardId, Deck, DeckId, Reviewable, ReviewableId


def reviewable_from_dto(dto: ReviewableDTO) -> Reviewable:
    return Reviewable(
        reviewable_id=ReviewableId(dto.id),
        answer=dto.answer,
        question=dto.question,
        review_at=dto.review_after,
        correct_answers=dto.correct_answers,
    )


def deck_from_dto(deck_dto: DeckDTO) -> Deck:
    return Deck(
        deck_id=DeckId(deck_dto.id),
        cards=defaultdict(
            set,
            {
                FlashcardId(flashcard_id): {reviewable_from_dto(reviewable) for reviewable in reviewables}
                for flashcard_id, reviewables in deck_dto.cards
            }
        ),
        name=deck_dto.name,
    )


def flashcard_from_dto(dto: FlashcardDTO) -> Flashcard:
    return Flashcard(
        flashcard_id=FlashcardId(dto.id),
        front=dto.front,
        back=dto.back,
    )
