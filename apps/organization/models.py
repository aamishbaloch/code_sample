from django.db import models
from model_utils.models import TimeStampedModel

from apps.base.models import ActiveStatusModel


class Organization(TimeStampedModel, ActiveStatusModel):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.name
