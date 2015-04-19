from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.utils.html import escape

from core import models
from nucleus.models import User
from api import model_constants as MC
from notifications.models import Notification

ResponseTypeChoices = (
  ('feedback','Feedback'),
  ('help','Help')
)

class Response(models.Model):
  user = models.ForeignKey(User, blank=True, null=True)
  text = models.TextField()
  app = models.CharField(max_length=15, blank=True)
  response_type = models.CharField(max_length=MC.CODE_LENGTH, choices=ResponseTypeChoices)
  resolved = models.BooleanField(default=False)
  email = models.EmailField(blank=True) # for anonymous user

  class Meta:
    ordering=['-id']

  def save(self, *args, **kwargs):
    flag = True if self.app=='Channel I Login' else False
    result = super(Response, self).save(*args, **kwargs)
    if not Notification.filter(app='helpcenter', instance=self).exists():
      if flag:
        Notification.save_notification('helpcenter', "A user "+escape(self.text[0].lower()+self.text[1:]).replace('\n','<br>'),
            '#helpcenter/exact/'+str(self.pk), Group.objects.get(name='Helpcenter Admin').user_set.all(), self)
      else:
        Notification.save_notification('helpcenter', self.user.html_name+(' gave a feedback: ' if\
            self.response_type=='feedback' else ' asked for help: ')+\
            "<div class='sub-text'>"+escape(self.text).replace('\n','<br>')+"</div>",
            '#helpcenter/exact/'+str(self.pk),
            Group.objects.get(name='Helpcenter Admin').user_set.all(), self)
    return result

  def delete(self, *args, **kwargs):
    self.reply_set.all().delete()
    Notification.delete_notification('helpcenter', self)
    return super(Response,self).delete(*args, **kwargs)

  def no_of_replies(self):
    return self.reply_set.count()

  def last_replied_by_IMG(self):
    if self.no_of_replies() == 0:
      return False
    u = self.reply_set.all().order_by('-number')[0].user
    return True if u.in_group('Helpcenter Admin') else False

  def __unicode__(self):
    return self.text[:50]

class Reply(models.Model):
  user = models.ForeignKey(User)
  by_img = models.BooleanField(default=False)
  response = models.ForeignKey(Response)
  number = models.IntegerField()
  text = models.TextField()

  class Meta:
    verbose_name_plural = 'Replies'
    ordering = ['number']

  def clean(self,**kwargs):
    if not (self.user == self.response.user or self.user.in_group('Helpcenter Admin')):
      raise ValidationError("User has not permission to reply")
    else:
      return super(Reply,self).clean(**kwargs)

  def save(self, *args, **kwargs):
    self.number = self.response.no_of_replies()+1
    self.by_img = self.user.in_group('Helpcenter Admin') and ((
        not self.response.user) or (not self.response.user.in_group('Helpcenter Admin')))
    result = super(Reply, self).save(*args, **kwargs)
    if self.user.in_group('Helpcenter Admin'):
      if self.response.user:
        Notification.save_notification('helpcenter', "IMG replied on your query :<div class='sub-text'>"+\
            escape(self.text).replace('\n','<br>')+"</div>",
            '#helpcenter/exact/'+str(self.response.pk), [self.response.user], self)
    else:
      Notification.save_notification('helpcenter', self.user.html_name + " replied on query :<div class='sub-text'>"+\
          escape(self.text).replace('\n','<br>')+"</div>", '#helpcenter/exact/'+str(self.response.pk),
          Group.objects.get(name='Helpcenter Admin').user_set.all(), self)
    return result

  def showname(self):
    return "IMG" if self.by_img else "Me"

  def showname_forIMG(self):
    return "IMG" if self.by_img else self.user

  def __unicode__(self):
    return self.text[:50]
