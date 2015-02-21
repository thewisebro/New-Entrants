from datetime import datetime

from django.contrib.sessions.models import Session

from core import models
from nucleus.models import User


class UserSession(models.Model):
  user = models.ForeignKey(User)
  session_key = models.CharField(max_length=40)
  ip = models.CharField(max_length=40)
  browser = models.CharField(max_length=40)
  os = models.CharField(max_length=40)


class PasswordCheck(models.Model):
  user = models.ForeignKey(User)
  service = models.CharField(max_length=40)
  seconds = models.PositiveIntegerField()

  @classmethod
  def exists_for(cls, user, service):
    instances = cls.objects.filter(user=user,
        service=service).order_by('-datetime_created')
    if instances.exists():
      instance = instances.first()
      now = datetime.now()
      span = now - instance.datetime_created
      if span.total_seconds() < instance.seconds:
        return True
    return False
