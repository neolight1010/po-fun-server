import django.urls as urls

from django.test import TestCase
from django.test.client import Client
from sample.models import Sample

from user.models import User
from vote.direction import Direction
from vote.models import Vote


class VoteViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_requires_login(self) -> None:
        response = self.client.post(self._vote_view_url(0), {"direction": 0})

        self.assertEqual(response.status_code, 302)

    def test_validates_missing_sample(self) -> None:
        self.client.force_login(self._simple_user())

        response = self.client.post(self._vote_view_url(
            0), {"direction": Direction.UP})

        self.assertEqual(response.status_code, 400)

    def test_upvote(self) -> None:
        user = self._simple_user()
        self.client.force_login(user)

        sample = Sample.objects.create(
            author=User.objects.create(username="John"))
        self.client.post(self._vote_view_url(sample.id), {
            "direction": Direction.UP})

        self.assertTrue(Vote.objects.filter(
            sample=sample, direction=Direction.UP, user=user).exists())

    def _vote_view_url(self, sample_id: int) -> str:
        return urls.reverse("vote:vote", args=[sample_id])

    def _simple_user(self) -> User:
        return User.objects.create()
