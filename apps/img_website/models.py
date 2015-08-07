from core import models, forms
from nucleus.models import User, Student, Role
from django.conf import settings

from redactor.fields import RedactorField
from crop_image import CropImage

import datetime

class MemberPhoto(CropImage):
  unique_name = 'teammember_member_pic'
  field_name = 'member_pic'
  width = 224
  height = 270

  @classmethod
  def get_instance(cls, request, pk):
    return request.user.student.teammember_set.all()[0]

  @classmethod
  def get_image_url(cls, image_field):
    if image_field:
      return image_field.instance.member_pic.url
    else:
      return settings.STATIC_URL + 'images/default_dp.png'

  @classmethod
  def file_name(cls, image_field, fname):
    if image_field.instance.member_pic:
      url_image = image_field.instance.member_pic.url
    else:
      url_image = "img_website/team/" + image_field.instance.member_name.user.username + "_1.jpg"
    previous_name = url_image.split(".")[0]
    prev_name = previous_name.split("/")[-1]
    if "_" in prev_name:
      new_number = str(int(prev_name.split("_")[-1]) + 1)
    else:
      new_number = "1"
    fname = image_field.instance.member_name.user.username + '_' + new_number + '.' +fname.split('.')[-1]
    return fname

class BlogPost(models.Model):
  title = models.CharField(max_length = 100, unique = True)
  short_description = models.TextField()
  content = RedactorField(redactor_options={'lang':'en'},
                          upload_to = 'img_website/redactor/',
                          allow_file_upload = True,
                          allow_image_upload = True
            )
  author = models.ForeignKey(User)
  state = models.CharField(max_length=12,
                           choices=(
                              ('Published', 'Published'),
                              ('Unpublished', 'Unpublished'),
                           ),
                           default='Unpublished')
  slug = models.SlugField(max_length = 150)

  def save(self, *args, **kwargs):
    self.slug=self.title.replace(' ','-')
    if(self.state=="Unpublished"):
      self.datetime_created=datetime.datetime.now()
    super(BlogPost, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.title


class PostCreateForm(forms.ModelForm):
  class Meta:
    model = BlogPost
    exclude = ('state','slug', 'author', 'date')
    widgets = {
      'short_description' : forms.Textarea(attrs = {'rows':2,'placeholder':'Short Description'}),
      'title' : forms.TextInput(attrs = {'placeholder':'Title'}),
    }
class PostUpdateForm(forms.ModelForm):
  class Meta:
    model = BlogPost
    exclude = ('state','slug','date', 'author')
    widgets = {
      'short_description' : forms.Textarea(attrs = {'rows':2,'placeholder':'Short Description'}),
      'title' : forms.TextInput(attrs = {'placeholder':'Title'}),
    }
class TeamMember(models.Model):
  member_name = models.ForeignKey(Student, unique = True)
  member_pic =  MemberPhoto.ModelField(
                           upload_to = 'img_website/team/',
                           blank = True,
          )
  member_post = models.CharField(max_length = 20,
                                 choices=(
                                   ('Developer', 'Developer'),
                                   ('Designer', 'Designer'),
                                 ),
                                 default = 'Developer')
  member_status = models.CharField(max_length = 20,
                                 choices=(
                                   ('Current', 'Current'),
                                   ('Alumni', 'Alumni'),
                                 ),
                                 default = 'Current')
  member_about = models.CharField(max_length = 200)

  def __unicode__(self):
    student = Student.objects.get(user_id = self.member_name)
    return student.name

class MemberLinks(models.Model):
  #name = models.CharField(max_length = 100)
  teammember = models.ForeignKey(TeamMember)
  website = models.CharField(max_length = 100,
                              choices=(
                                ('facebook', 'Facebook'),
                                ('quora', 'Quora'),
                                ('twitter', 'Twitter'),
                                ('googleplus', 'Google Plus'),
                                ('github', 'Github'),
                                ('linkedin', 'LinkedIn'),
                              ),
                            )
  link = models.URLField()

  def __unicode__(self):
    student = Student.objects.get(user_id = self.teammember.member_name)
    return student.name + '_' + self.website

class AddMemberForm(forms.ModelForm):
  class Meta:
    model = TeamMember
    exclude = ('member_name', 'member_pic')
    widgets = {
      'member_about' : forms.Textarea(attrs = {'rows':3,'placeholder':'Write about yourself in not more than 200 words...'}),
    }

class AddPicForm(forms.ModelForm):
  class Meta:
    model = TeamMember
    exclude = ('member_name',)
    widgets = {
      'member_about' : forms.Textarea(attrs = {'rows':3}),
    }

class RecentWorks(models.Model):
  title = models.CharField(max_length = 100, unique = True)
  image = models.ImageField(
                           upload_to = 'img_website/works/',
          )
  short_description = models.TextField()
  content = RedactorField(redactor_options={'lang':'en'},
                          upload_to=settings.MEDIA_ROOT + 'img_website/redactor/',
                          allow_file_upload=True,
                          allow_image_upload=True
            )
  author = models.ForeignKey(User)
  state = models.CharField(max_length=12,
                           choices=(
                              ('Published', 'Published'),
                              ('Unpublished', 'Unpublished'),
                           ),
                           default='Unpublished')
  category = models.CharField(max_length=12,
                           choices=(
                              ('Intranet', 'Intranet'),
                              ('Internet', 'Internet'),
                           ),
                           default='Intranet')

  slug = models.SlugField(max_length = 150)

  def save(self, *args, **kwargs):
    self.slug=self.title.replace(' ','-')
    if(self.state=="Unpublished"):
      self.datetime_created=datetime.datetime.now()
    super(RecentWorks, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.title

class WorkCreateForm(forms.ModelForm):
  class Meta:
    model = RecentWorks
    exclude = ('state','slug', 'author', 'date')
    widgets = {
      'short_description' : forms.Textarea(attrs = {'rows':2,'placeholder':'Short Description'}),
      'title' : forms.TextInput(attrs = {'placeholder':'Title'}),
    }
class WorkUpdateForm(forms.ModelForm):
  class Meta:
    model = RecentWorks
    exclude = ('state','slug','date', 'author')
    widgets = {
      'short_description' : forms.Textarea(attrs = {'rows':2,'placeholder':'Short Description'}),
      'title' : forms.TextInput(attrs = {'placeholder':'Title'}),
    }
class Contact(models.Model):
  name = models.CharField(max_length = 50)
  email = models.EmailField(max_length = 100)
  message = models.TextField()

class ContactForm(forms.ModelForm):
  class Meta:
    model = Contact
    widgets = {
      'name' : forms.TextInput(attrs = {'placeholder':'Name'}),
      'email' : forms.TextInput(attrs = {'placeholder':'Email'}),
      'message' : forms.Textarea(attrs = {'rows':3}),
    }

class StatusPost(models.Model):
  content = RedactorField(redactor_options={'lang':'en'},
                          upload_to=settings.MEDIA_ROOT + 'img_website/redactor/',
                          allow_file_upload=True,
                          allow_image_upload=True
            )
  state = models.CharField(max_length=12,
                           choices=(
                              ('Published', 'Published'),
                              ('Unpublished', 'Unpublished'),
                           ),
                           default='Unpublished')

  author = models.ForeignKey(User)
  app = models.CharField(max_length = 40)

  def __unicode__(self):
    return self.content[:200]

  def save(self, *args, **kwargs):
    if(self.state=="Unpublished"):
      self.datetime_created=datetime.datetime.now()
    super(StatusPost, self).save(*args, **kwargs)

class StatusPostCreateForm(forms.ModelForm):
  class Meta:
    model = StatusPost
    exclude = ('state', 'author', 'date')
    widgets = {
      'app' : forms.TextInput(attrs = {'placeholder':'App Name'}),
    }

class StatusPostUpdateForm(forms.ModelForm):
  class Meta:
    model = StatusPost
    exclude = ('state','date', 'author')
    widgets = {
      'app' : forms.TextInput(attrs = {'placeholder':'App Name'}),
    }


