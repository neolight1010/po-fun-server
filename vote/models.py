from django.db import models
from sample.models import Sample

from user.models import User


class Vote(models.Model):
    class Direction(models.IntegerChoices):
        UP = 0
        DOWN = 1

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    direction = models.IntegerField(choices=Direction.choices)
