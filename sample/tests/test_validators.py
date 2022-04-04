from unittest.mock import MagicMock
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from sample.models import Sample
from django.contrib.staticfiles import finders


_UNALLOWED_TYPE_FRAGMENT = "Allowed types are"


class SampleValidatorsTestCase(TestCase):
    author = get_user_model()()

    def setUp(self) -> None:
        self.author.save()

        return super().setUp()

    def test_valid_mp3(self):
        mp3_sample = Sample(
            name="test file",
            author=self.author,
            sample_type=Sample.SampleType.MELODIC,
            sample_file=finders.find("sample/test_files/audio.mp3"),
        )

        mp3_sample.save()
        self.assertTrue(mp3_sample.sample_file)

        try:
            mp3_sample.full_clean()
        except ValidationError as e:
            errors = e.message_dict.get("sample_file")

            if not errors:
                return

            self.assertFalse(
                any(
                    [_UNALLOWED_TYPE_FRAGMENT in error for error in errors]
                )
            )

    def test_non_audio_file(self):
        found_file = finders.find("sample/test_files/image.png")

        non_audio_sample = Sample(
            name="test file",
            author=self.author,
            sample_type=Sample.SampleType.MELODIC,
            sample_file=found_file,
        )
        non_audio_sample.save()

        try:
            non_audio_sample.full_clean()
        except ValidationError as e:
            errors = e.message_dict["sample_file"]

            self.assertTrue(
                any(
                    [_UNALLOWED_TYPE_FRAGMENT in error for error in errors]
                )
            )
