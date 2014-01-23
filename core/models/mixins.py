from datetime import datetime

from django.conf import settings

from taggit_autocomplete.managers import TaggableManager
from core import models


class Taggable(models.Model):
  tags = TaggableManager()

  class Meta:
    abstract = True


class TrashableManager(models.Manager):
  use_for_related_fields = True
  def get_query_set(self):
    return super(TrashableManager, self).get_query_set().filter(trashed=False)

class TrashedManager(models.Manager):
  def get_query_set(self):
    return super(TrashableManager, self).get_query_set().filter(trashed=True)

class Trashable(models.Model):
  trashed = models.BooleanField(default=False)
  datetime_trashed = models.DateTimeField(blank=True, null=True)
  objects = TrashableManager()
  trashed_objects = TrashedManager()

  def trash(self):
    if not self.trashed:
      self.datetime_trashed = datetime.now()
    self.trashed = True
    self.save()

  class Meta:
    abstract = True
