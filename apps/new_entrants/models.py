from core import models
from nucleus.models import User, Branch
from groups.models import Group
from api import model_constants as MC

class Student_profile(models.Model):
    user = models.OneToOneField(User)
    branch = models.ForeignKey(Branch, blank = True)
    email = models.EmailField(max_length = 75)
    fb_link = models.CharField(max_length = 200)
    state = models.CharField(max_length = 3, choices = MC.STATE_CHOICES, blank = True)
    hometown = models.CharField(max_length = 100, blank = True)
    phone_no = models.CharField(max_length = 20)
    phone_privacy = models.BooleanField(default = False)
    profile_privacy = models.BooleanField(default = False)
    def __unicode__(self):
        return str(self.user.name)

class Senior_profile(models.Model):
    user = models.OneToOneField(User)
    branch = models.ForeignKey(Branch)
    email = models.EmailField(max_length = 75)
    hometown = models.CharField(max_length = 100, blank = True)
    state = models.CharField(max_length = 3, choices = MC.STATE_CHOICES, blank = True)
    fb_link = models.CharField(max_length = 200)
    phone_no = models.CharField(max_length = 20)
    def __unicode__(self):
        return str(self.user.name)

class Blogs(models.Model):
    group = models.ForeignKey(Group)
    content = models.TextField()
    title = models.CharField(max_length = 200)
    date_published = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return "%s : %s" % str(self.group.nickname),str(self.title)

class Requests(models.Model):
    student_profile = models.ForeignKey(Student_profile)
    senior_profile = models.ForeignKey(Senior_profile)
    is_accepted = models.BooleanField(default = False)
