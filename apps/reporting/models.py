from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings

from core import models


class Report(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  description = models.TextField()
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content = generic.GenericForeignKey('content_type', 'object_id')


class Reportable(models.Model):
  reports = generic.GenericRelation(Report)

  class Meta:
    abstract = True
