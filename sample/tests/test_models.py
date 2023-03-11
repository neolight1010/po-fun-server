from django.test import TestCase

from sample.models import Sample
from vote.direction import Direction
from vote.models import Vote
from user.models import User


class SampleTests(TestCase):
    def test_points_up(self) -> None:
        sample = Sample.objects.create(author=User.objects.create(username="User 1"))

        Vote.objects.create(
            sample=sample,
            user=User.objects.create(username="User 2"),
            direction=Direction.UP,
        )

        self.assertEqual(sample.points, 1)

    def test_points_down(self) -> None:
        sample = Sample.objects.create(author=User.objects.create(username="User 1"))

        Vote.objects.create(
            sample=sample,
            user=User.objects.create(username="User 2"),
            direction=Direction.DOWN,
        )

        self.assertEqual(sample.points, -1)
