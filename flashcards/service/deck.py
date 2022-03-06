import datetime
from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

from flashcards.domain.flashcard import Deck, DeckId, FlashcardId, ReviewableId
from flashcards.uow import UnitOfWork


def create_deck(name: str, uow: UnitOfWork) -> UUID:
    with uow:
        if (deck := uow.repositories.deck.find_by_name(name)) is not None:
            return deck.id
        deck_id = uuid4()
        uow.repositories.deck.add(Deck(deck_id=DeckId(deck_id), name=name))
        uow.commit()
    return deck_id


def add_flashcard_to_deck(flashcard_id: UUID, deck_name: str, both_sides: bool, uow: UnitOfWork) -> None:
    with uow:
        flashcard = uow.repositories.flashcard.get(flashcard_id=FlashcardId(flashcard_id))
        deck = uow.repositories.deck.find_by_name(deck_name)
        if deck is None:
            raise ValueError
        deck.add_card(flashcard=flashcard, both_sides=both_sides)
        uow.repositories.deck.add(deck)
        uow.commit()


@dataclass(frozen=True)
class ReviewableDTO:
    id: UUID
    question: str
    answer: str


def get_next_reviewable(deck_name: str, uow: UnitOfWork) -> Optional[ReviewableDTO]:
    with uow:
        deck = uow.repositories.deck.find_by_name(deck_name)
        if deck is None:
            raise ValueError
        all_reviewables = deck.cards_to_review(datetime=datetime.datetime.now())
    return next(iter(all_reviewables), None)


def mark_correct(deck_name: str, reviewable_id: UUID, correct: bool, uow: UnitOfWork) -> None:
    with uow:
        deck = uow.repositories.deck.find_by_name(deck_name)
        if deck is None:
            raise ValueError
        if correct:
            deck.mark_correct(reviewable_ids={ReviewableId(reviewable_id)})
        else:
            deck.mark_incorrect(reviewable_ids={ReviewableId(reviewable_id)})
        uow.repositories.deck.add(deck)
        uow.commit()
