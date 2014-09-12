from core import models
from core.forms import ModelForm
from nucleus.models import User
from datetime import datetime
from core.models.fields import CKEditorField
from django.core.cache import cache, get_cache
import simplejson

from notices.constants import *
from notices.constants import *

class AbstractNotice(models.Model):
  subject = models.CharField(max_length=100)
  reference = models.CharField(max_length=100, blank=True)
  expire_date = models.DateField()
  content = CKEditorField()
  uploader = models.ForeignKey('Uploader')
  emailsend = models.BooleanField(default=False)
  re_edited = models.BooleanField(default=False)
  expired_status = models.BooleanField(default=False)
  datetime_modified = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True

  def __unicode__(self):
    return unicode(self.pk)

class Notice(AbstractNotice):
  pass

class TrashNotice(AbstractNotice):
  notice_id = models.IntegerField()
  editing_no = models.IntegerField()
  original_datetime = models.DateTimeField()

class NoticeUser(models.Model):
  user = models.OneToOneField(User)
  categories = models.ManyToManyField('Category')
  subscribed = models.BooleanField(default = False)
  read_notices = models.ManyToManyField(Notice, related_name = 'read_noticeuser_set', blank=True, null=True)
  starred_notices = models.ManyToManyField(Notice, related_name = 'starred_noticeuser_set', blank=True, null=True)

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
  main_category = models.CharField(max_length=20)
  name = models.CharField(max_length=100)
  code = models.CharField(max_length=100, unique=True)

  class Meta:
    verbose_name_plural = "Categories"

  def __unicode__(self):
    return self.name

  def save(self):
    super(Category, self).save()
    Category.set_cache()

  def delete(self):
    super(Category, self).delete()
    Category.set_cache()

  @classmethod
  def set_cache(self):
    mc = {'order' : []}
    for c in Category.objects.all():
      if(c.main_category not in mc):
        mc[c.main_category] = []
        mc['order'].append(c.main_category)
      mc[c.main_category].append(c.name)
    for i in mc['order']:
      if len(mc[i])==1 and mc[i][0]=='All':
        mc[i] = []
    mc['order'] = sorted(mc['order'])
    t=0
    for num in range(len(mc['order'])):
        if mc[mc['order'][num]]==[]:
          mc['order'].insert(t, mc['order'][num])
          del mc['order'][num+1]
          t = t+1
    cache.set('main_categories_cached', simplejson.dumps(mc))
