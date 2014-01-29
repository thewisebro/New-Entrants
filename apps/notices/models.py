from core import models
from core.forms import ModelForm
from nucleus.models import User
from datetime import datetime
from core.models.fields import CKEditorField
from notices.constants import *

class Notice(models.Model):
class AbstractNotice(models.Model):
  subject = models.CharField(max_length=100)
  reference = models.CharField(max_length=100, blank=True)
  expire_date = models.DateField()
  content = CKEditorField()
  uploader = models.ForeignKey('Uploader')
  emailsend = models.BooleanField(default=False)
  re_edited = models.BooleanField(default=False)
  expired_status = models.BooleanField(default=True)
  datetime_modified = models.DateTimeField(auto_now=True)

  def __unicode__(self):
    return unicode(self.pk)

  expired_status = models.BooleanField(default=False)
  datetime_modified = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

  def __unicode__(self):
    return unicode(self.pk)

class Notice(AbstractNotice):
  pass

class Old_Notice(AbstractNotice):
  notice_id = models.IntegerField()
  editing_no = models.IntegerField()

class NoticeUser(models.Model):
  user = models.OneToOneField(User)
  categories = models.ManyToManyField('Category')
  subscribed = models.BooleanField(default = False)
  read_notices = models.ManyToManyField(Notice, related_name = 'read_noticeuser_set')
  starred_notices = models.ManyToManyField(Notice, related_name = 'starred_noticeuser_set')

  def __unicode__(self):
	return unicode(self.user)

class Uploader(models.Model):
  user= models.ForeignKey(User)
  name= models.CharField(max_length=100)
  category = models.ForeignKey('Category')

  def __unicode__(self):
    return str(self.user) + ':' + str(self.category)

class Category(models.Model):
  users = models.ManyToManyField(User, through='Uploader')
  main_category = models.CharField(max_length=10,choices = OPTIONS)
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=100)

  def __unicode__(self):
    return self.name

