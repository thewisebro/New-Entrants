from datetime import datetime

from taggit_autocomplete.managers import TaggableManager
from django.db import models
from base import Manager

class Taggable(models.Model):
  tags = TaggableManager()

  class Meta:
    abstract = True


class TrashableQueryset(models.QuerySet):
  def all_items(self):
    return self.filter(trashed=False)

  def all_trashed_items(self):
    return self.filter(trashed=True)

  def trash(self):
    for item in self:
      item.trash()
  trash.queryset_only = True

  def restore(self):
    for item in self:
      item.restore()
  restore.queryset_only = True


class TrashableManager(Manager):
  use_for_related_fields = True

class NonTrashedItemsManager(Manager):
  def get_queryset(self):
    return TrashableQueryset(self.model, using=self._db).all_items()

class TrashedItemsManager(Manager):
  def get_queryset(self):
    return TrashableQueryset(self.model, using=self._db).all_trashed_items()

class Trashable(models.Model):
  trashed = models.BooleanField(default=False)
  datetime_trashed = models.DateTimeField(blank=True, null=True)
  objects = TrashableManager.from_queryset(TrashableQueryset)()
  items = NonTrashedItemsManager.from_queryset(TrashableQueryset)()
  trashed_items = TrashedItemsManager.from_queryset(TrashableQueryset)()

  def trash(self):
    if not self.trashed:
      self.datetime_trashed = datetime.now()
      self.trashed = True
      self.save()

  def restore(self):
    if self.trashed:
      self.datetime_trashed = None
      self.trashed = False
      self.save()

  class Meta:
    abstract = True
