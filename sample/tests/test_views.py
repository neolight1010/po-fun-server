from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Final, cast

from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.fields import Field
from django.test.testcases import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from sample.forms.SampleForm import SampleForm
from sample.models import Sample, Tag
from sample.tests.mock_sample_file import MOCK_SAMPLE_FILE
from sample.views import upload
from vote.direction import Direction
from vote.models import Vote

from user.models import User

if TYPE_CHECKING:
    from django.test.client import _MonkeyPatchedWSGIResponse


class UploadViewsTestCase(TestCase):
    _UPLOAD_URL = reverse("sample:upload")

    def setUp(self) -> None:
        self.user = User.objects.create(username="test")
        self.client.force_login(self.user)

    def test_should_redirect_to_login(self):
        self.client.logout()

        response = self.client.get(self._UPLOAD_URL, follow=True)

        self.assertRedirects(
            response, reverse("app:login") + f"?next={self._UPLOAD_URL}"
        )

    def test_should_return_200_when_authenticated(self):
        response = self.client.get(self._UPLOAD_URL)
        self.assertEquals(response.status_code, 200)

    def test_get_request(self):
        response = self.client.get(self._UPLOAD_URL)

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

        response = self.client.post(self._UPLOAD_URL, data=form.data)

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

        request = RequestFactory().post(self._UPLOAD_URL, data=form.data)
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

        request = RequestFactory().post(self._UPLOAD_URL, data=form.data)
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


class SamplesViewSearchTests(TestCase):
    _DRUMS_URL = reverse("sample:drums")

    def setUp(self) -> None:
        self.author = User.objects.create(username="author")

    def test_unfiltered_samples(self) -> None:
        sample = self._create_simple_sample()

        response = self.client.get(self._DRUMS_URL)

        samples = response.context.get("sample_list") or []

        self._assert_found_sample(samples, sample)

    def test_filtered_samples_by_name(self) -> None:
        searchable_sample = self._create_sample_searchable_by_name()
        self._create_simple_sample()

        response = self.client.get(self._DRUMS_URL, data={"search": "searchable"})

        samples = response.context.get("sample_list") or []

        self._assert_found_sample(samples, searchable_sample)

    def test_filtered_samples_by_tag(self) -> None:
        searchable_sample = self._create_sample_searchable_by_tag()
        self._create_simple_sample()

        response = self.client.get(self._DRUMS_URL, data={"search": "searchable"})

        samples = response.context.get("sample_list") or []

        self._assert_found_sample(samples, searchable_sample)

    def _create_simple_sample(self):
        return Sample.objects.create(
            name="Some Sample",
            author=self.author,
            sample_type=Sample.SampleType.DRUM,
            sample_file=SimpleUploadedFile(
                name="sample name", content=MOCK_SAMPLE_FILE
            ),
        )

    def _create_sample_searchable_by_name(self):
        searchable_sample = Sample.objects.create(
            name="Searchable Sample",
            author=self.author,
            sample_type=Sample.SampleType.DRUM,
            sample_file=SimpleUploadedFile(
                name="sample name", content=MOCK_SAMPLE_FILE
            ),
        )
        return searchable_sample

    def _create_sample_searchable_by_tag(self):
        searchable_sample = Sample.objects.create(
            name="Sample Name",
            author=self.author,
            sample_type=Sample.SampleType.DRUM,
            sample_file=SimpleUploadedFile(
                name="sample name", content=MOCK_SAMPLE_FILE
            ),
        )

        searchable_sample.tags.add(Tag.objects.create(name="searchable"))
        return searchable_sample

    def _assert_found_sample(self, samples: list[Sample], sample: Sample) -> None:
        self.assertEqual(len(samples), 1)
        self.assertEqual(samples[0], sample)


class SamplesViewOrderTests(TestCase):
    _DRUMS_URL: Final = reverse("sample:drums")

    def setUp(self) -> None:
        self.author = User.objects.create(username="author")

        self.first_sample = self._create_simple_sample(name="First Sample")
        self.second_sample = self._create_simple_sample(name="Second Sample")

        self._order_samples_opposite_to_default_ordering()

    def test_order_by_most_recent_is_default(self) -> None:
        self._make_first_sample_the_newest()

        response = self.client.get(self._DRUMS_URL)

        self._assert_response_has_samples_in_correct_order(response)

    def test_order_by_least_recent(self) -> None:
        self._make_first_sample_the_oldest()

        response = self.client.get(self._DRUMS_URL, data={"order": "least-recent"})

        self._assert_response_has_samples_in_correct_order(response)

    def test_order_by_most_recent(self) -> None:
        self._make_first_sample_the_newest()

        response = self.client.get(self._DRUMS_URL, data={"order": "most-recent"})

        self._assert_response_has_samples_in_correct_order(response)

    def test_order_by_least_points(self) -> None:
        self._make_first_sample_the_least_voted()

        response = self.client.get(self._DRUMS_URL, data={"order": "least-points"})

        self._assert_response_has_samples_in_correct_order(response)

    def test_order_by_most_points(self) -> None:
        self._make_first_sample_the_most_voted()

        response = self.client.get(self._DRUMS_URL, data={"order": "most-points"})

        self._assert_response_has_samples_in_correct_order(response)

    def _create_simple_sample(self, *, name: str = "Some Sample") -> Sample:
        sample = Sample.objects.create(
            name=name,
            author=self.author,
            sample_type=Sample.SampleType.DRUM,
            sample_file=SimpleUploadedFile(
                name="sample name", content=MOCK_SAMPLE_FILE
            ),
        )

        sample.created_at = dt.datetime(2023, 1, 1, tzinfo=dt.timezone.utc)
        sample.save()

        return sample

    def _make_first_sample_the_oldest(self) -> None:
        self.first_sample.created_at = self.second_sample.created_at - dt.timedelta(
            days=1
        )
        self.first_sample.save()

    def _make_first_sample_the_newest(self) -> None:
        self.first_sample.created_at = self.second_sample.created_at + dt.timedelta(
            days=1
        )
        self.first_sample.save()

    def _order_samples_opposite_to_default_ordering(self) -> None:
        self._make_first_sample_the_oldest()

    def _make_first_sample_the_least_voted(self) -> None:
        Vote.objects.create(
            sample=self.first_sample, user=self.author, direction=Direction.DOWN
        )

    def _make_first_sample_the_most_voted(self) -> None:
        Vote.objects.create(
            sample=self.first_sample, user=self.author, direction=Direction.UP
        )

    def _assert_response_has_samples_in_correct_order(
        self, response: _MonkeyPatchedWSGIResponse
    ) -> None:
        response_samples = list(response.context.get("object_list") or [])

        self.assertEqual(
            response_samples,
            [self.first_sample, self.second_sample],
            "Samples are not the same or in the expected order.",
        )
