from django.contrib.sessions.models import Session

from core import models
from nucleus.models import User

class UserSession(models.Model):
  user = models.ForeignKey(User)
  session_key = models.CharField(max_length=40)
  ip = models.CharField(max_length=40)
  browser = models.CharField(max_length=40)
  os = models.CharField(max_length=40)
