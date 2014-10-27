from core import models
from core.models.mixins import Taggable
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from nucleus.models import User,Student
from api import model_constants as MC

from taggit_autocomplete.managers import TaggableManager

class post(models.Model):
  text_content = models.CharField(max_length=200)
  tags = TaggableManager()
  # images=models.ManyToManyField('Image')
  post_date = models.DateTimeField(auto_now=True)
  user_tags = models.ManyToManyField(Student)
  def __unicode__(self):
    return self.text_content






