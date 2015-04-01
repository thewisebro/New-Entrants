from core import models
from core.models.mixins import Taggable
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from nucleus.models import User,Student
from api import model_constants as MC
from yaadein import constants as YC

from taggit_autocomplete.managers import TaggableManager

class YaadeinUser(models.Model):
  """
    This inherited child of 'User' model is to bind all those
    user attributes which are specific to Yaadein app
  """
  user = models.OneToOneField(User)
  coverpic = models.FileField(upload_to='yaadein/coverpic/', null=True, blank=True)
  status = models.CharField(max_length = 200, choices=YC.YAADEIN_USER_STATUS, default='A')  # Default is 'Active'
  def __unicode__(self):
    return self.user.name

class Spot(models.Model):
  name = models.CharField(max_length = 200, null=True)
  tagline = models.CharField(max_length = 200, null=True)
  profile_pic = models.FileField(upload_to='yaadein/spot/', null=True, blank=True)
  coverpic = models.FileField(upload_to='yaadein/coverpic/',null =True, blank=True)
  def __unicode__(self):
    return self.name

class Post(models.Model):
  text_content = models.CharField(max_length=200)
  tags = TaggableManager()
  #images=models.ManyToManyField('Image')
  spots = models.ManyToManyField(Spot)
  upvote = models.IntegerField(default=0)
  post_date = models.DateTimeField(auto_now=True)
  user_tags = models.ManyToManyField(Student, related_name="tagged_user")
  owner = models.ForeignKey(Student, related_name="post_owner")
  wall_user = models.ForeignKey(Student, related_name="post_wall_user")
  status = models.CharField(max_length = 200, choices=YC.POST_STATUS, default='A') # Default is 'Active'
  def __unicode__(self):
    return self.text_content

class PostImage(models.Model):
  image = models.FileField(upload_to='yaadein/')
  post = models.ForeignKey(Post)
  def __unicode__(self):
    return self.image.url

