import django.db.models as models

class Direction(models.IntegerChoices):
    UP = 0
    DOWN = 1
