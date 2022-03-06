from uuid import UUID, uuid4

from flashcards.domain.flashcard import Flashcard, FlashcardId
from flashcards.uow import UnitOfWork


def add_flashcard(front: str, back: str, uow: UnitOfWork) -> UUID:
    flashcard_id = uuid4()
    with uow:
        uow.repositories.flashcard.add(Flashcard(front=front, back=back, flashcard_id=FlashcardId(flashcard_id)))
        uow.commit()
    return flashcard_id
