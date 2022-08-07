from django.test import Client, SimpleTestCase
from django.urls import reverse

class IndexViewTests(SimpleTestCase):
    def test_response_200(self):
        client = Client()

        response = client.get(reverse("app:index"))
        
        self.assertEqual(response.status_code, 200)

class LoginViewTests(SimpleTestCase):
    def test_response_200(self):
        client = Client()

        response = client.get(reverse("app:login"))
        
        self.assertEqual(response.status_code, 200)
