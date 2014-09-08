from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from core import models
from core.models.mixins import Trashable
from nucleus.models import User
from moderation.models import Reportable
import api.model_constants as MC

class Feed(models.Model, Reportable):
  app = models.CharField(max_length=MC.CODE_LENGTH)
  user = models.ForeignKey(User, blank=True, null=True)
  content = models.TextField(blank=True)
  instance_type = models.ForeignKey(ContentType, blank=True, null=True)
  instance_id = models.PositiveIntegerField(blank=True, null=True)
  instance = generic.GenericForeignKey('instance_type', 'instance_id')
  link = models.CharField(max_length=200, blank=True)
  dummy = models.BooleanField(default=False)
  shown_feed = models.ForeignKey('Feed', blank=True, null=True, related_name='dependent_feeds')
  tags = models.ManyToManyField('FeedTag', blank=True, null=True)
  last_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return self.content[:250]

  class Meta:
    ordering = ['-last_modified']

class FeedTag(models.Model):
  key = models.CharField(max_length=MC.CODE_LENGTH)
  value = models.CharField(max_length=200)
  class Meta:
    unique_together = ['key', 'value']
