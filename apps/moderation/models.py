from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.db import models as djangomodels

from core import models

class Report(models.Model):
  reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reports')
  description = models.TextField(blank=True)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content = generic.GenericForeignKey('content_type', 'object_id')
  flagged = models.NullBooleanField(blank=True, null=True)
  moderated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                                    related_name='moderated_reports')

class Reportable(djangomodels.Model):
  reports = generic.GenericRelation(Report)

  class Meta:
    abstract = True
