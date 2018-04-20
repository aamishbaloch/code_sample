from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.base.fields import StatusField


class ActiveStatusModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """
    active = StatusField(_('active'))

    class Meta:
        abstract = True
