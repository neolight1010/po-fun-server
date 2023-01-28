from typing import Callable
from typing_extensions import Self
import django.urls as urls

from django.test import TestCase
from django.test.client import Client

from sample.models import Sample
from user.models import User
from vote.models import Vote


class VoteViewTests(TestCase):
    def test_requires_login(self) -> None:
        client = Client()

        response = client.post(self._vote_view_url(0), {"direction": 0})

        self.assertEqual(response.status_code, 302)

    def test_validates_schema(self) -> None:
        client = Client()

        client.force_login(self._simple_user())

        response = client.post(self._vote_view_url(0), {"direction": Vote.Direction.UP})

        self.assertEqual(response.status_code, 400)

    def _vote_view_url(self, sample_id: int) -> str:
        return urls.reverse("vote:vote", args=[sample_id])

    def _simple_user(self) -> User:
        user = User()
        user.save()

        return user
