from django.db import models
from upload_validator import FileTypeValidator

from user.models import User

from .validators import validate_pack_sample_length

ALLOWED_FILE_TYPES = ["audio/wav", "audio/ogg", "audio/mpeg"]


class Sample(models.Model):
    class SampleType(models.TextChoices):
        MELODIC = "MELODIC"
        DRUM = "DRUM"
        PACK = "PACK"

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    sample_type = models.CharField(
        max_length=10, choices=SampleType.choices
    )

    demo = models.FileField(
        upload_to="uploads/",
        validators=[FileTypeValidator(
            allowed_types=ALLOWED_FILE_TYPES)],
        blank=True
    )

    # TODO: validate length only for pack samples.
    sample_file = models.FileField(
        upload_to="uploads/",
        validators=[FileTypeValidator(
            allowed_types=ALLOWED_FILE_TYPES), validate_pack_sample_length],
    )

    def __str__(self) -> str:
        return self.name
