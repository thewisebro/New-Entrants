from core import models
from nucleus.models import Student
from api import model_constants as MC

class GameScore(models.Model):
  student = models.ForeignKey(Student)
  gamecode = models.CharField(max_length=MC.TEXT_LENGTH)
  score = models.IntegerField()

class GameSession(models.Model):
  student = models.ForeignKey(Student)
  gamecode = models.CharField(max_length=MC.TEXT_LENGTH)
  gsession = models.CharField(max_length=MC.TEXT_LENGTH)
  start_time = models.DateTimeField(auto_now_add=True)
  authkey = models.CharField(max_length=MC.TEXT_LENGTH)
