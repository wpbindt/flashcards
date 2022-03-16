import unittest
from typing import Set

from flashcards.container import get_fake_uow
from flashcards.service.deck import create_deck, add_flashcard_to_deck, remove_flashcard_from_decks, ReviewableDTO, \
    get_next_reviewable
from flashcards.service.flashcard import add_flashcard


class TestDeck(unittest.TestCase):
    @staticmethod
    def _get_all_reviewables(deck_name: str) -> Set[ReviewableDTO]:
        output: Set[ReviewableDTO] = set()
        while (reviewable := get_next_reviewable(deck_name=deck_name, uow=get_fake_uow())) not in output:
            assert reviewable is not None
            output.add(reviewable)
        return output

    def test_removing_flashcard_from_decks_removes_flashcard_from_decks(self) -> None:
        deck_name1 = 'test-deck1'
        deck_name2 = 'test-deck2'
        create_deck(name=deck_name1, uow=get_fake_uow())
        create_deck(name=deck_name2, uow=get_fake_uow())
        removed_flashcard_id = add_flashcard(front='unimportant', back='also unimportant', uow=get_fake_uow())
        unremoved_flashcard_id = add_flashcard(front='unimportant', back='also unimportant', uow=get_fake_uow())

        add_flashcard_to_deck(removed_flashcard_id, deck_name=deck_name1, both_sides=False, uow=get_fake_uow())
        add_flashcard_to_deck(unremoved_flashcard_id, deck_name=deck_name2, both_sides=False, uow=get_fake_uow())
        add_flashcard_to_deck(unremoved_flashcard_id, deck_name=deck_name1, both_sides=False, uow=get_fake_uow())
        remove_flashcard_from_decks(flashcard_id=removed_flashcard_id, uow=get_fake_uow())

        for reviewables in map(self._get_all_reviewables, {deck_name1, deck_name2}):
            self.assertEqual(len(reviewables), 1)
