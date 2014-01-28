import datetime

from core import models
from core.models import mixins
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from nucleus.models import Student
from api import model_constants as MC

from taggit_autocomplete.managers import TaggableManager

class Question(mixins.Taggable):
  profile = models.ForeignKey('Profile')
  datetime = models.DateTimeField(auto_now_add=True)
  description = models.TextField()
  title = models.CharField(max_length=MC.TEXT_LENGTH)

  def __unicode__(self):
    return self.title


class Profile(models.Model):
  student = models.OneToOneField(Student, primary_key=True)
  tags_followed = TaggableManager()
  questions_followed = models.ManyToManyField(Question, null=True, blank=True, related_name='following_profiles')
  answers_up = models.ManyToManyField('Answer', null=True, blank=True, related_name='upvoted_by')
  answers_down = models.ManyToManyField('Answer', null=True, blank=True, related_name='downvoted_by')

  def __unicode__(self):
    return self.student.username

  @staticmethod
  def get_profile(student):
    try:
      return student.profile
    except Profile.DoesNotExist:
      return Profile.objects.create(student=student)

class Answer(models.Model):
  profile = models.ForeignKey(Profile)
  question = models.ForeignKey(Question)
  description = models.TextField()
  datetime = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.description


class Activity(models.Model):
  ASK_QUES = 'ASK_QUES'
  POST_ANS = 'POST_ANS'
  FOLLOW_TOPIC = 'FOL_TOPIC'
  FOLLOW_QUES = 'FOL_QUES'
  ACTIVITY_CHOICES = (
    (ASK_QUES, 'Asked Question'),
    (POST_ANS, 'Posted Answer'),
    (FOLLOW_TOPIC, 'Followed Topic'),
    (FOLLOW_QUES, 'Followed question')
  )
  activity_type = models.CharField(max_length=MC.CODE_LENGTH, choices=ACTIVITY_CHOICES)
  content_type = models.ForeignKey(ContentType)
  object_id = models.IntegerField()
  content = generic.GenericForeignKey('content_type','object_id')
  profile = models.ForeignKey(Profile)
  datetime = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.profile + ':' + self.activity_type

