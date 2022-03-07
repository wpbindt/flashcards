import unittest
from datetime import datetime
from uuid import uuid4

from freezegun import freeze_time

from flashcards.domain.flashcard import Flashcard, FlashcardId, Deck, DeckId


class TestDeck(unittest.TestCase):
    @freeze_time('1970-2-3 19:58:00')
    def test_added_flashcards_are_scheduled_immediately(self) -> None:
        flashcard = Flashcard(flashcard_id=FlashcardId(uuid4()), front='bla', back='di')
        deck = Deck(deck_id=DeckId(uuid4()), name='bla')

        deck.add_card(flashcard)

        self.assertEqual(
            len(deck.cards_to_review(datetime=datetime.now())),
            1
        )

    @freeze_time('1970-2-3 19:58:00')
    def test_added_flashcards_have_front_as_answer_by_default(self) -> None:
        flashcard = Flashcard(flashcard_id=FlashcardId(uuid4()), front='bla', back='di')
        deck = Deck(deck_id=DeckId(uuid4()), name='bla')
        deck.add_card(flashcard)

        reviewable = deck.cards_to_review(datetime.now()).pop()

        self.assertEqual(
            reviewable.answer,
            flashcard.back
        )
        self.assertEqual(
            reviewable.question,
            flashcard.front
        )

    @freeze_time('1970-2-3 19:58:00')
    def test_can_add_flashcards_for_both_sides(self) -> None:
        flashcard = Flashcard(flashcard_id=FlashcardId(uuid4()), front='bla', back='di')
        deck = Deck(deck_id=DeckId(uuid4()), name='bla')
        deck.add_card(flashcard, both_sides=True)

        reviewable1, reviewable2 = deck.cards_to_review(datetime.now())

        self.assertEqual(reviewable1.answer, reviewable2.question)
        self.assertEqual(reviewable2.answer, reviewable1.question)
