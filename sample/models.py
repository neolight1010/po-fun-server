from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class Sample(models.Model):
    class SampleType(models.TextChoices):
        MELODIC = _("MELODIC")
        DRUM = _("DRUM")

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    sample_type = models.CharField(
        max_length=10, choices=SampleType.choices, name="type"
    )
    sample_file = models.FileField(upload_to="uploads/", name="file")
