from typing import cast
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.fields import Field
from django.test.testcases import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from sample.forms.SampleForm import SampleForm
from sample.models import Sample
from sample.tests.mock_sample_file import MOCK_SAMPLE_FILE
from sample.views import upload

from user.models import User


_UPLOAD_URL = reverse("sample:upload")


class UploadViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test")
        self.client.force_login(self.user)

    def test_should_redirect_to_login(self):
        self.client.logout()

        response = self.client.get(_UPLOAD_URL, follow=True)

        self.assertRedirects(response, reverse("app:login") + f"?next={_UPLOAD_URL}")

    def test_should_return_200_when_authenticated(self):
        response = self.client.get(_UPLOAD_URL)
        self.assertEquals(response.status_code, 200)

    def test_get_request(self):
        response = self.client.get(_UPLOAD_URL)

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
        form = SampleForm(data={"invalid": "data"})

        response = self.client.post(_UPLOAD_URL, data=form.data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(Sample.objects.count(), 0)

    def test_post_request_valid_data(self) -> None:
        form = SampleForm(
            data={
                "name": "sample name",
                "description": "sample description",
                "sample_type": Sample.SampleType.DRUM,
                "demo": "",
                "tags": "tag1",
            }
        )

        request = RequestFactory().post(_UPLOAD_URL, data=form.data)
        request.user = self.user
        request.FILES["sample_file"] = SimpleUploadedFile(
            name="test", content=MOCK_SAMPLE_FILE
        )

        response = upload(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("app:index"))

        if (sample := Sample.objects.first()) is None:
            self.fail("Sample not created.")
        else:
            self.assertEqual(sample.name, "sample name")
            self.assertEqual(sample.description, "sample description")
            self.assertEqual(sample.sample_type, Sample.SampleType.DRUM)

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

        self.assertTrue(sample.tags.filter(name="tag1").exists())
        self.assertTrue(sample.tags.filter(name="tag2").exists())
        self.assertTrue(sample.tags.filter(name="tag3").exists())
