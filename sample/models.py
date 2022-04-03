from django.db import models
from django.contrib.auth import get_user_model
from upload_validator import FileTypeValidator

from .validators import validate_pack_sample_length


class Sample(models.Model):
    allowed_file_types = ["audio/wav", "audio/ogg", "audio/mpeg"]

    class SampleType(models.TextChoices):
        MELODIC = "MELODIC"
        DRUM = "DRUM"
        PACK = "PACK"

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    sample_type = models.CharField(
        max_length=10, choices=SampleType.choices, name="type"
    )

    demo = models.FileField(
        upload_to="uploads/",
        validators=[FileTypeValidator(
            allowed_types=allowed_file_types)],
        blank=True
    )

    # TODO: validate length only for pack samples.
    sample_file = models.FileField(
        upload_to="uploads/",
        name="file",
        validators=[FileTypeValidator(
            allowed_types=allowed_file_types), validate_pack_sample_length],
    )

    def __str__(self) -> str:
        return self.name
