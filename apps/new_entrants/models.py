from core import models
from nucleus.models import User, Branch
from groups.models import Group
from api import model_constants as MC

class Student_profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(max_length = 75)
    fb_link = models.CharField(max_length = 200, blank = True)
    state = models.CharField(max_length = 3, choices = MC.STATE_CHOICES)
    hometown = models.CharField(max_length = 100, blank = True)
    phone_no = models.CharField(max_length = 20, blank = True)
    phone_privacy = models.BooleanField(default = False)
    profile_privacy = models.BooleanField(default = False)
    is_branch = models.BooleanField(default = False)
    def __unicode__(self):
        return str(self.user.username) + ":" + str(self.user.name)

class Senior_profile(models.Model):
    user = models.OneToOneField(User)
    email = models.EmailField(max_length = 75)
    hometown = models.CharField(max_length = 100, blank = True)
    state = models.CharField(max_length = 3, choices = MC.STATE_CHOICES)
    fb_link = models.CharField(max_length = 200, blank = True)
    phone_no = models.CharField(max_length = 20, blank = True)
    def __unicode__(self):
        return str(self.user.username) + ":" + str(self.user.name)

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique=True)
    group = models.ForeignKey(Group)
    description = models.CharField(max_length = 250, blank = True, null = True)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField(max_length = 150)

    def save(self, *args, **kwargs):
      self.slug=self.title.replace(' ','-')
      super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.group.user.username) + ":" + str(self.title)

class Request(models.Model):
    senior = models.ForeignKey(Senior_profile, related_name='to')
    junior = models.ForeignKey(Student_profile, related_name='from')
    is_accepted = models.BooleanField(default = False)

    class Meta:
      ordering = ('-datetime_created',)

    def __unicode__(self):
        return str(self.junior.user.username) + "-->" + str(self.senior.user.username)
