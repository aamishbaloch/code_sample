from django.db import models
from model_utils.models import TimeStampedModel

from apps.base.models import ActiveStatusModel
from apps.organization.models import Organization


class Job(TimeStampedModel, ActiveStatusModel):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    organization = models.ForeignKey(Organization, related_name='job', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
