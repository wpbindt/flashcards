import argparse
import sys

from flashcards.container import get_pg_uow
from flashcards.service.flashcard import add_flashcard
from flashcards.service.deck import create_deck as create_deck_service, \
    add_flashcard_to_deck, get_next_reviewable, mark_correct


def print_help() -> None:
    print('TODO write help message')


def review() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    args = parser.parse_args(sys.argv[2:])
    while True:
        reviewable_dto = get_next_reviewable(deck_name=args.name, uow=get_pg_uow())
        if reviewable_dto is None:
            print('No more cards to review!')
            exit(0)
        print(f'Front: {reviewable_dto.question} <<press enter to see answer>>')
        input()
        print(f'Back: {reviewable_dto.answer} (correct? [y/N])')
        response = input()
        correct = response.lower() in {'yes', 'y'}
        mark_correct(deck_name=args.name, reviewable_id=reviewable_dto.id, correct=correct, uow=get_pg_uow())


def create_deck() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    args = parser.parse_args(sys.argv[2:])
    if args.name:
        create_deck_service(name=args.name, uow=get_pg_uow())


def add_card() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--front')
    parser.add_argument('--back')
    parser.add_argument('--deck')
    parser.add_argument('--both-sides', action='store_true')
    args = parser.parse_args(sys.argv[2:])
    flashcard_id = add_flashcard(front=args.front, back=args.back, uow=get_pg_uow())
    add_flashcard_to_deck(
        flashcard_id=flashcard_id,
        deck_name=args.deck,
        both_sides=args.both_sides,
        uow=get_pg_uow(),
    )


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_help()
    elif sys.argv[1] == '--deck':
        review()
    elif sys.argv[1] == 'create-deck':
        create_deck()
    elif sys.argv[1] == 'add':
        add_card()
