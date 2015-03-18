from core import models
from api import model_constants as MC
from nucleus.models import User, Student, Role

class Group(Role('Student Group')):
  '''
    Group Details
  '''
  nickname = models.CharField(max_length=MC.TEXT_LENGTH)
  website = models.URLField(blank=True)
  description = models.TextField(blank=True)
  admin = models.ForeignKey(Student, related_name="student_group_set", blank=True, null=True)
  is_active = models.BooleanField(default=False)

  def __unicode__(self):
    return str(self.user.name)

  def save(self,*args,**kwargs):
    return_value = super(Group,self).save(*args, **kwargs)
    groupinfo, created = GroupInfo.objects.get_or_create(group=self)
    if created:
      post = Post.objects.create(post_name = 'Member')
      if self.admin:
        Membership.objects.create(student=self.admin, post=post, groupinfo=groupinfo)
    return return_value


class Post(models.Model):
  post_name = models.CharField(max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return str(self.post_name)


class GroupInfo(models.Model):
  """
    Information of a Group
  """
  group = models.OneToOneField('Group', primary_key=True)
  mission = models.TextField(blank=True, null=True)
  founding_year = models.CharField(max_length=MC.TEXT_LENGTH, null=True, blank=True)
  members = models.ManyToManyField(Student, related_name="groupinfos", through="Membership")
  posts = models.ManyToManyField(Post)
  subscribers= models.ManyToManyField(User, blank=True)
  facebook_url = models.URLField(blank=True)
  twitter_url = models.URLField(blank=True)
  gplus_url = models.URLField(blank=True)
  def __unicode__(self):
    return str(self.group)

class Membership(models.Model):
  post = models.ForeignKey(Post)
  student = models.ForeignKey(Student)
  groupinfo = models.ForeignKey(GroupInfo)
  def __unicode__(self):
    return str(self.groupinfo)

class GroupActivity(models.Model):
  group = models.ForeignKey(Group)
  text = models.TextField()

  class Meta:
    ordering = ['-id']
