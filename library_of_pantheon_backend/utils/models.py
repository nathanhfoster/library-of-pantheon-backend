from django.db import models
from django.conf import settings
from .managers import ArchivedManager

class AbstractArchivedModel(models.Model):
    """ Implements soft delete """
    archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(blank=True, null=True)

    objects = ArchivedManager()

    class Meta:
        abstract = True


class TimeStampAbstractModel(models.Model):
    """ Inherit from this class to add timestamp fields in the model class """

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class OwnerAbstractModel(models.Model):
    """ Implements logging of creation and modification """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_creator",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updator",
    )

    class Meta:
        abstract = True
