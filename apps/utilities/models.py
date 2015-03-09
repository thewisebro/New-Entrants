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

class UserEmail(models.Model):
  user = models.ForeignKey(User)
  email = models.EmailField(max_length = 255)
  verified = models.BooleanField(default = False)
  confirmation_key = models.CharField(max_length = 40, blank= True)
  last_datetime_created = models.DateTimeField(null = True, blank=True)
  verify_num = models.IntegerField(default=0)

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

class PasswordReset(models.Model):
  user = models.ForeignKey(User)
#reset_done = models.BooleanField(default = False)
  reset_key = models.CharField(max_length = 40, blank= True)
  last_datetime_created = models.DateTimeField(null = True, blank=True)
  verify_num = models.IntegerField(default=0)

