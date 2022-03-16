import datetime
import unittest
import uuid
from math import floor
from typing import List

from freezegun import freeze_time

from flashcards.domain.reviewable import Reviewable, ReviewableId


class TestReviewable(unittest.TestCase):
    def test_reviewables_sorted_by_review_after_date(self) -> None:
        reviewable1 = Reviewable(
            reviewable_id=ReviewableId(uuid.uuid4()),
            answer='unimportant',
            question='also-unimportant',
            review_at=datetime.datetime(1970, 1, 1, 0, 0, 0),
        )
        reviewable2 = Reviewable(
            reviewable_id=ReviewableId(uuid.uuid4()),
            answer='unimportant',
            question='also-unimportant',
            review_at=datetime.datetime(1970, 1, 2, 0, 0, 0),
        )
        reviewable3 = Reviewable(
            reviewable_id=ReviewableId(uuid.uuid4()),
            answer='unimportant',
            question='also-unimportant',
            review_at=datetime.datetime(1970, 1, 1, 0, 1, 0),
        )

        sorted_reviewables = sorted({reviewable1, reviewable2, reviewable3})

        expected = [reviewable1, reviewable3, reviewable2]
        self.assertEqual(
            sorted_reviewables,
            expected
        )

    @freeze_time('1970-1-3 02:03:01')
    def test_mark_incorrect_immediately_reschedules(self) -> None:
        reviewable = Reviewable(
            reviewable_id=ReviewableId(uuid.uuid4()),
            answer='unimportant',
            question='also-unimportant',
            review_at=datetime.datetime(1970, 1, 1, 0, 0, 0),
        )

        reviewable.mark_incorrect()

        self.assertEqual(
            reviewable.review_at,
            datetime.datetime(1970, 1, 3, 0, 0, 0)
        )

    @freeze_time('1970-1-3 02:03:01')
    def test_mark_correct_reschedules_exponentially(self) -> None:
        reviewable = Reviewable(
            reviewable_id=ReviewableId(uuid.uuid4()),
            answer='unimportant',
            question='also-unimportant',
            review_at=datetime.datetime(1970, 1, 1, 0, 0, 0),
        )

        rescheduled_times: List[datetime.datetime] = []
        for _ in range(1, 6):
            reviewable.mark_correct()
            rescheduled_times.append(reviewable.review_at)

        expected = [
            datetime.datetime(1970, 1, 3, 0, 0, 0) + datetime.timedelta(days=i)
            for i in [floor(Reviewable.REVIEW_INTERVAL_EXPONENT ** n) - 1 for n in range(1, 6)]
        ]
        self.assertEqual(
            rescheduled_times,
            expected,
        )
