from django.core.exceptions import ValidationError
from django.db import models
from upload_validator import FileTypeValidator

from user.models import User

from .validators import validate_pack_sample_length

ALLOWED_FILE_TYPES = ["audio/wav", "audio/ogg", "audio/mpeg", "audio/x-wav"]


class Sample(models.Model):
    class SampleType(models.TextChoices):
        MELODIC = "MELODIC"
        DRUM = "DRUM"
        PACK = "PACK"

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    sample_type = models.CharField(max_length=10, choices=SampleType.choices)

    demo = models.FileField(
        upload_to="uploads/",
        validators=[FileTypeValidator(allowed_types=ALLOWED_FILE_TYPES)],
        blank=True,
    )

    sample_file = models.FileField(
        upload_to="uploads/",
        validators=[FileTypeValidator(allowed_types=ALLOWED_FILE_TYPES)],
    )

    def clean(self) -> None:
        if self.sample_type == self.SampleType.PACK:
            try:
                validate_pack_sample_length(self.sample_file)
            except ValidationError as e:
                raise ValidationError({"sample_file": e.message})

    def __str__(self) -> str:
        return self.name
