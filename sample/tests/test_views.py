from typing import cast
from unittest.mock import MagicMock, Mock, patch
from django.forms.fields import Field
from django.test.testcases import TestCase
from django.test.client import Client
from django.urls.base import reverse
from sample.forms.SampleForm import SampleForm
from sample.models import Sample

from user.models import User


UPLOAD_URL = reverse("sample:upload")


class UploadViewsTestCase(TestCase):
    user: User

    def setUp(self) -> None:
        self.user = User.objects.create(username="test")

        return super().setUp()

    def test_should_redirect_to_login(self):
        client = Client()
        response = client.get(UPLOAD_URL, follow=True)

        redirected_url, redirected_status = response.redirect_chain[-1]

        self.assertEquals(redirected_status, 302)
        self.assertTrue(redirected_url.startswith(reverse("app:login")))

    def test_should_return_200_when_authenticated(self):
        client = Client()
        client.force_login(self.user)

        response = client.get(UPLOAD_URL)
        self.assertEquals(response.status_code, 200)

    def test_get_request(self):
        client = Client()
        client.force_login(self.user)

        response = client.get(UPLOAD_URL)

        form = response.context.get("form")
        self.assertIsInstance(form, SampleForm)

        form = cast(SampleForm, form)
        with self.subTest("field labels should be lowercase"):
            for field in form.fields.values():
                field = cast(Field, field)

                self.assertIsNotNone(field.label)

                label = cast(str, field.label)

                self.assertTrue(label.islower())

    def test_post_request_invalid_data(self):
        client = Client()
        client.force_login(self.user)

        pre_request_samples_quantity = len(Sample.objects.all())

        response = client.post(UPLOAD_URL)
        self.assertEquals(response.status_code, 200)

        post_request_samples_quantity = len(Sample.objects.all())

        self.assertEquals(pre_request_samples_quantity,
                          post_request_samples_quantity)

    @patch("sample.views.SampleForm")
    def test_post_request_valid_data(self, mock_SampleForm: MagicMock):
        client = Client()
        client.force_login(self.user)

        mock_sample = Mock()

        mock_sample_form = MockSampleForm(mock_sample)
        mock_SampleForm.return_value = mock_sample_form

        response = client.post(UPLOAD_URL, follow=True)

        self.assertEquals(response.redirect_chain[-1][0], reverse("app:index"))

        self.assertEquals(mock_sample_form.save.call_count, 1)
        self.assertEquals(mock_sample.author, self.user)


class MockSampleForm():
    def __init__(self, mock_sample: Mock):
        self.save = Mock(return_value=mock_sample)
        self.save_m2m = Mock()

    def is_valid(self):
        return True
