from django.test import Client, SimpleTestCase
from django.urls import reverse

class IndexViewTests(SimpleTestCase):
    def test_not_404(self):
        client = Client()

        response = client.get(reverse("app:index"))
        
        self.assertNotEqual(response.status_code, 404)
