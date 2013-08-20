import datetime

from core import models
from nucleus.models import Student
from api import model_constants as MC

from taggit_autocomplete.managers import TaggableManager

class Question(models.Taggable):
  author = models.ForeignKey(Profile)
  datetime = models.DateTimeField(auto_now_add=True)
  description = models.TextField()
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return self.topic


class Profile(models.Model):
  student = models.OneToOneField(Student, primary_key=True)
  tags_followed = TaggableManager()
  questions_followed = models.ManyToManyField(Question,null=True, blank=True)
  answers_up = models.ManyToManyField(Answer, null=True, blank=True)
  answers_down = models.ManyToManyField(Answer, null=True, blank=True)
  def __unicode__(self):
    return self.student.username

class Answer(models.Model):
  question = models.ForeignKey(Question)
  description = models.TextField()
  datetime = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.description
# Create your models here.
