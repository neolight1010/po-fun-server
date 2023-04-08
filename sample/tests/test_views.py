from typing import cast
from unittest.mock import MagicMock, Mock, patch
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.fields import Field
from django.test.testcases import TestCase
from django.test.client import Client, RequestFactory
from django.urls.base import reverse

from sample.forms.SampleForm import SampleForm
from sample.models import Sample
from sample.tests.mock_sample_file import MOCK_SAMPLE_FILE
from sample.views import upload

from user.models import User


_UPLOAD_URL = reverse("sample:upload")


class UploadViewsTestCase(TestCase):
    user: User

    def setUp(self) -> None:
        self.user = User.objects.create(username="test")

        return super().setUp()

    def test_should_redirect_to_login(self):
        client = Client()
        response = client.get(_UPLOAD_URL, follow=True)

        self.assertRedirects(response, reverse("app:login") + f"?next={_UPLOAD_URL}")

    def test_should_return_200_when_authenticated(self):
        client = Client()
        client.force_login(self.user)

        response = client.get(_UPLOAD_URL)
        self.assertEquals(response.status_code, 200)

    def test_get_request(self):
        client = Client()
        client.force_login(self.user)

        response = client.get(_UPLOAD_URL)

        form = response.context[0].get("form")
        self.assertIsInstance(form, SampleForm)

        form = cast(SampleForm, form)
        with self.subTest("field labels should be lowercase"):
            for field in form.fields.values():
                field = cast(Field, field)

                self.assertIsNotNone(field.label)

                label = cast(str, field.label)

                self.assertTrue(label.islower(), f"Label '{label}' is not lowercase")

    def test_post_request_invalid_data(self):
        client = Client()
        client.force_login(self.user)

        pre_request_samples_quantity = len(Sample.objects.all())

        response = client.post(_UPLOAD_URL)
        self.assertEquals(response.status_code, 400)

        post_request_samples_quantity = len(Sample.objects.all())

        self.assertEquals(pre_request_samples_quantity, post_request_samples_quantity)

    @patch("sample.views.SampleForm")
    def test_post_request_valid_data(self, mock_SampleForm: MagicMock):
        client = Client()
        client.force_login(self.user)

        mock_sample = Mock()

        mock_sample_form = MockSampleForm(mock_sample)
        mock_SampleForm.return_value = mock_sample_form

        response = client.post(_UPLOAD_URL, follow=True)

        self.assertRedirects(response, reverse("app:index"))

        self.assertEquals(mock_sample_form.save.call_count, 1)
        self.assertEquals(mock_sample.author, self.user)

    def test_tags_are_created(self) -> None:
        form = SampleForm(
            data={
                "name": "test",
                "description": "test",
                "sample_type": Sample.SampleType.DRUM,
                "demo": "",
                "tags": "tag1, tag2, tag3",
            }
        )

        request = RequestFactory().post(_UPLOAD_URL, data=form.data)
        request.user = self.user
        request.FILES["sample_file"] = SimpleUploadedFile(
            name="test", content=MOCK_SAMPLE_FILE
        )

        upload(request)

        sample = Sample.objects.first()

        if sample is None:
            self.fail("Sample was not created.")

        self.assertIsNotNone(sample.tags.filter(name="tag1").first())
        self.assertIsNotNone(sample.tags.filter(name="tag2").first())
        self.assertIsNotNone(sample.tags.filter(name="tag3").first())


class MockSampleForm:
    def __init__(self, mock_sample: Mock):
        self.save = Mock(return_value=mock_sample)
        self.save_m2m = Mock()

        self.cleaned_data = {"tags": ""}

    def is_valid(self):
        return True
