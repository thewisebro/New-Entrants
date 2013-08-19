from taggit_autocomplete.managers import TaggableManager

from django.db import models

class Taggable(models.Model):
  tags = TaggableManager()

  class Meta:
    abstract = True
