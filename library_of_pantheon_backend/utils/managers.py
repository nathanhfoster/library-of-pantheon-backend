from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class ArchivedQuerySet(QuerySet):
    def delete(self):
        self.update(archived=True, archived_date=timezone.now())

    def undelete(self):
        self.update(archived=False)

    def real_delete(self):
        return super().delete()


class ArchivedManager(models.Manager):
    def get_queryset(self):
        # filter archived items
        return ArchivedQuerySet(self.model, using=self._db).filter(archived=False)

    def all_plus_deleted(self, *args, **kwargs):
        # all items archived = True + archived = False
        return ArchivedQuerySet(self.model, using=self._db)

    def archived(self, *args, **kwargs):
        # only archived=True items
        return ArchivedQuerySet(self.model, using=self._db).filter(archived=True)
