from django.test import Client, SimpleTestCase
from django.urls import reverse


class IndexViewTests(SimpleTestCase):
    def test_response_200(self):
        client = Client()

        response = client.get(reverse("app:index"))

        self.assertEqual(response.status_code, 200)


class RegisterViewTests(SimpleTestCase):
    def test_get_response_200(self):
        client = Client()

        response = client.get(reverse("app:register"))

        self.assertEqual(response.status_code, 200)

    def test_post_response_200(self):
        client = Client()

        response = client.post(reverse("app:register"))

        self.assertEqual(response.status_code, 200)
