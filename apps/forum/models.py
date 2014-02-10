import datetime

from core import models
from core.models.mixins import Taggable
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from nucleus.models import Student
from api import model_constants as MC

from taggit_autocomplete.managers import TaggableManager

class Question(Taggable):
  profile = models.ForeignKey('Profile')
  datetime_modified = models.DateTimeField(auto_now=True)
  description = models.TextField()
  title = models.CharField(max_length=MC.TEXT_LENGTH)

  def save(self,*args,**kwargs):
    result = super(Question,self).save(*args,**kwargs)
    if not Activity.objects.filter(activity_type=Activity.ASK_QUES,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).exists():
      Activity.objects.create(activity_type=Activity.ASK_QUES, content=self)
    return result

  def delete(self,*args,**kwargs):
    if Activity.objects.filter(activity_type=Activity.ASK_QUES,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).exists():
      Activity.objects.filter(activity_type=Activity.ASK_QUES,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).delete()
    result = super(Question,self).delete(*args,**kwargs)
    return result

  def __unicode__(self):
    return self.title


class Profile(models.Model):
  student = models.OneToOneField(Student, primary_key=True)
  tags_followed = TaggableManager()
  questions_followed = models.ManyToManyField(Question, null=True, blank=True,
      through='ProfileQuestionFollowed', related_name='following_profiles')
  answers_up = models.ManyToManyField('Answer', null=True, blank=True,
      through='ProfileAnswerUpvoted', related_name='upvoted_by')
  answers_down = models.ManyToManyField('Answer', null=True, blank=True, related_name='downvoted_by')

  def __unicode__(self):
    return self.student.user.username

  @staticmethod
  def get_profile(student):
    try:
      return student.profile
    except Profile.DoesNotExist:
      return Profile.objects.create(student=student)

class ProfileQuestionFollowed(models.Model):
  profile = models.ForeignKey(Profile)
  question = models.ForeignKey(Question)

  def save(self,*args,**kwargs):
    result = super(ProfileQuestionFollowed,self).save(*args,**kwargs)
    Activity.objects.create(activity_type=Activity.FOLLOW_QUES, content=self)
    return result

  def delete(self,*args,**kwargs):
    if Activity.objects.filter(activity_type=Activity.FOLLOW_QUES,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).exists():
      Activity.objects.filter(activity_type=Activity.FOLLOW_QUES,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).delete()

    result  = super(ProfileQuestionFollowed,self).delete(*args,**kwargs)
    return result

  def __unicode__(self):
    return unicode(self.profile) + '->' + unicode(self.question)

  class Meta:
    db_table = 'forum_profile_questions_followed'

class ProfileAnswerUpvoted(models.Model):
  profile = models.ForeignKey(Profile)
  answer = models.ForeignKey('Answer')

  def save(self,*args,**kwargs):
    result = super(ProfileAnswerUpvoted,self).save(*args,**kwargs)
    Activity.objects.create(activity_type=Activity.UPVOTE_ANS, content=self)
    return result

  def delete(self,*args,**kwargs):
    if Activity.objects.filter(activity_type=Activity.UPVOTE_ANS,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).exists():
      Activity.objects.filter(activity_type=Activity.UPVOTE_ANS,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).delete()

    result  = super(ProfileAnswerUpvoted,self).delete(*args,**kwargs)
    return result

  def __unicode__(self):
    return unicode(self.profile) + '->' + unicode(self.answer)

  class Meta:
    db_table = 'forum_profile_answers_up'

class Answer(models.Model):
  profile = models.ForeignKey(Profile)
  question = models.ForeignKey(Question)
  description = models.TextField()
  datetime_modified = models.DateTimeField(auto_now=True)
  def save(self,*args,**kwargs):
    result = super(Answer,self).save(*args,**kwargs)
    Activity.objects.create(activity_type=Activity.POST_ANS, content=self)
    return result

  def delete(self,*args,**kwargs):
    if Activity.objects.filter(activity_type=Activity.POST_ANS,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).exists():
      Activity.objects.filter(activity_type=Activity.POST_ANS,
        content_type=ContentType.objects.get_for_model(self), object_id=self.pk).delete()

    result  = super(Answer,self).delete(*args,**kwargs)
    return result


  def __unicode__(self):
    return self.description


class Activity(models.Model):
  ASK_QUES = 'ASK_QUES'
  POST_ANS = 'POST_ANS'
  FOLLOW_TOPIC = 'FOL_TOPIC'
  FOLLOW_QUES = 'FOL_QUES'
  UPVOTE_ANS = 'UP_ANS'
  ACTIVITY_CHOICES = (
    (ASK_QUES, 'Asked Question'),
    (POST_ANS, 'Posted Answer'),
    (FOLLOW_TOPIC, 'Followed Topic'),
    (FOLLOW_QUES, 'Followed question'),
    (UPVOTE_ANS, 'Upvoted Answer')
  )
  activity_type = models.CharField(max_length=MC.CODE_LENGTH, choices=ACTIVITY_CHOICES)
  content_type = models.ForeignKey(ContentType)
  object_id = models.IntegerField()
  content = generic.GenericForeignKey('content_type','object_id')
  datetime = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return self.activity_type

