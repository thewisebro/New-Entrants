from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from core import models
from nucleus.models import User


class Notification(models.Model):
  app = models.CharField(max_length=15)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content = generic.GenericForeignKey('content_type', 'object_id')
  text = models.CharField(max_length=1000)
  url = models.URLField(blank=True, null=True)
  users = models.ManyToManyField(User, through='UserNotification')

  class Meta:
    ordering = ['-id']

  def __unicode__(self):
    return self.text[:200]

  @staticmethod
  def filter(app, instance):
    content_type = ContentType.objects.get_for_model(instance)
    return Notification.objects.filter(app=app, object_id=instance.pk, content_type=content_type)

  @staticmethod
  def save_notification(app, text, url, users, instance):
    content_type = None
    if instance:
      content_type = ContentType.objects.get_for_model(instance)
    notification = Notification(app=app, text=text, url=url, object_id=instance.pk, content_type=content_type)
    notification.save()
    for user in users:
      UserNotification.objects.get_or_create(user=user, notification=notification)
    return notification

  @staticmethod
  def delete_notification(app, instance):
    content_type = ContentType.objects.get_for_model(instance)
    notification = Notification.objects.get_or_none(app=app, object_id=instance.pk, content_type=content_type)
    if notification:
      notification.delete()

class UserNotification(models.Model):
  user = models.ForeignKey(User)
  notification = models.ForeignKey(Notification)
  viewed = models.BooleanField(default=False)

  class Meta:
    ordering = ['-id']

  def __unicode__(self):
    return unicode(self.user) + unicode(self.notification)
