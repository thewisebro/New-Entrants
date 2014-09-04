from django.db import models
from api import model_constants as MC, models as api_models
from nucleus.models import Person
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Group(models.Model):
  '''
    Group Details
  '''
  name = models.CharField(max_length=MC.TEXT_LENGTH)
  nickname = models.CharField(max_length=MC.TEXT_LENGTH)
  website = models.URLField(blank=True)
  description = models.TextField(blank=True)
  admin = models.ForeignKey(Person,related_name="student_group_set",blank=True,null=True)
  user = models.OneToOneField(User)
  is_active = models.BooleanField(default=False)

  def __unicode__(self):
    return str(self.name)

  def clean(self):
    if self.user.groups.filter(name='Student Group').count() == 0:
      raise ValidationError('Group Account MUST belong to the group: Student_groups')

  def save(self,*args,**kwargs):
    return_value = super(Group,self).save(*args,**kwargs) 
    group_info,created = GroupInfo.objects.get_or_create(group = self)
    if created:
      post = Post.objects.create(post_name = 'Member')
      if self.admin:
        Membership.objects.create(person = self.admin,post=post,groupinfo=group_info)
    return return_value

class Post(models.Model):
  post_name = models.CharField(max_length=MC.TEXT_LENGTH)
  def __unicode__(self):
    return str(self.post_name)


class GroupInfo(models.Model): 
  """
    Information of a Group
  """ 
  group = models.OneToOneField('Group')  
  mission = models.TextField(blank=True,null=True)
  founding_year = models.CharField(max_length=MC.TEXT_LENGTH,null=True,blank=True)
  phone_no = models.CharField(max_length=MC.PHONE_NO_LENGTH,null=True,blank=True)
  members = models.ManyToManyField(Person,related_name="groupinfos",through="Membership")
  posts = models.ManyToManyField(Post)  
  subscribers= models.ManyToManyField(User,blank= True)
  email = models.EmailField(blank=True,null=True)
  photo = models.ImageField(upload_to='groups/photo/', blank=True)
  def __unicode__(self):
    return str(self.group)

class Membership(models.Model):
  post = models.ForeignKey(Post)
  person = models.ForeignKey(Person)
  groupinfo = models.ForeignKey(GroupInfo)
  def __unicode__(self):
    return str(self.groupinfo)

class GroupActivity(models.Model):
  group = models.ForeignKey(Group)
  text = models.TextField()
  datetime = models.DateTimeField(auto_now_add = True)
  
  class Meta:
    ordering = ['-id']
