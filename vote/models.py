from django.db import models
from sample.models import Sample

from user.models import User
from vote.direction import Direction


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    direction = models.IntegerField(choices=Direction.choices)

    class Meta:
        unique_together = [["user", "sample"]]
