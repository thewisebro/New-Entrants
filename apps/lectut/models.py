from core import models
from core import forms

from nucleus.models import User , Course , Faculty , Batch
from threadedcomments.models import ThreadedComment

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save
from datetime import datetime, timedelta
import os

#from lectut.views import getFileType
from notifications.models import Notification

fs = FileSystemStorage(location='Uploads')

# Create your models here.

class TextNotice(models.Model):
  text=models.CharField(max_length=500 , null=False)
  upload_user=models.ForeignKey(User)
  batch=models.ForeignKey(Batch)

  def __unicode__(self):
    return str(self.text)

  def as_dict(self):
    fileData={
      'text':str(self.text),
      'upload_user':str(self.upload_user.name),
      'batch':str(self.batch)
    }
    return fileData

class BaseUpload(models.Model):
  class Meta:
    abstract = True

  """def save(self, *args, **kwargs):
     if self.featured:
          self.__class__.objects.all().update(featured = False)
     super(Model, self).save(*args, **kwargs)"""

'''Act_Types = (
            ('lec' , 'Lecture'),
            ('tut' , 'Tutorial'),
            ('sol' , 'Solution'),
            ('que' , 'Question'),
            ('exm' , 'Exam Papers')
            )
'''

# Each post attributes
class Post(models.Model):
  upload_user = models.ForeignKey(User)
  batch = models.ForeignKey(Batch)
  content = models.CharField(max_length = '1000')
  privacy = models.BooleanField(max_length = 3 , default = 'tut')

  def __unicode__(self):
    return str(self.content)

# Over-ridden to create notification
  def save(self, *args, **kwargs):
    post = super(Post , self).save(*args, **kwargs)
    currentBatch = Batch.objects.get(id = self.batch.id)
    students = currentBatch.students.all()
    users = map(lambda x:x.user, students)
    Notification.save_notification('lectut','The user ' +str(self.upload_user.name)+ ' uploaded a post','lectut/'+str(currentBatch.id)+'/upload',users,self)
    return post

  def as_dict(self):
    postData={
      'id':self.id,
      'upload_user': str(self.upload_user.name),
      'user_image': self.upload_user.photo_url(),
      'datetime_created':str(self.datetime_created),
      'batch':str(self.batch),
      'content':self.content,
      'privacy':self.privacy,
    }
    return postData

# Get path where uploaded file is saved
def upload_path(instance , filename ):
  return ('lectut/'+instance.file_type+'/'+filename)
#  return os.path.join('lectut/',instance.file_type,'/')


# Each file attributes
class Uploadedfile(BaseUpload):
  post = models.ForeignKey(Post)
  upload_file=models.FileField(upload_to= upload_path)
  description=models.CharField(max_length=100 , null=False)
  file_type=models.CharField(max_length=10 , null=False)
  upload_type=models.CharField(max_length=3 , default='tut')

  def __unicode__(self):
    return str(self.upload_file)

  def as_dict(self):
        filename = str(self.upload_file)
        filename = filename.split("/")[2]
        fileData={
           'id':self.id,
           'post':self.post.id,
           'upload_file':filename,
           'username':str(self.post.upload_user.name),
           'datetime_created':str(self.datetime_created),
           'description':self.description,
           'file_type':self.file_type,
           'upload_type':self.upload_type,
        }
        return fileData


class UploadFile(BaseUpload):
  upload_file=models.FileField(upload_to='lectut/images/')
  name=models.CharField(max_length=100 , null=False)
  file_type=models.CharField(max_length=10 , null=False)
  upload_type=models.CharField(max_length=3 , default='tut')
  privacy=models.BooleanField(default=False)      #false means visible to all
  upload_user=models.ForeignKey(User)
  batch=models.ForeignKey(Batch)

  '''def save(self, *args, **kwargs):
    uploadedFile = super(UploadFile , self).save(*args, **kwargs)
    currentBatch = Batch.objects.get(id = self.batch)
    students = currentBatch.students.all()
    notification.save_notification('lectut','The user' +self.upload_user+ 'uploaded a file','lectut/'+self.id+'/upload',students,self)
    return uploadFile'''

  def __unicode__(self):
    return str(self.upload_file)

  def as_dict(self):
    imageData={
      'upload_file':str(self.upload_file),
      'name':self.name,
      'file_type':self.file_type,
      'upload_type':self.upload_type,
      'privacy':self.privacy,
      'upload_user':str(self.upload_user.name),
      'batch':str(self.batch)
    }
    return imageData

class Reminders(models.Model):
  text = models.CharField(max_length=50 , null=False)
  event_date = models.DateTimeField(default = datetime.now()+timedelta(days=7))
  batch = models.ForeignKey(Batch)
  user = models.ForeignKey(User)

  def __unicode__(self):
    return str(self.text)

  def as_dict():
    reminder={
      'text':self.text,
      'event_date':str(self.event_date),
      'batch':str(self.batch),
      'user':str(self.user)
    }
    return reminder

class DownloadLog(models.Model):
  uploadfile = models.ForeignKey(Uploadedfile)
  user = models.ForeignKey(User)

  def __unicode__(self):
    return self.id

'''class UploadPdf(BaseUpload):
  upload_pdf=models.FileField(upload_to='lectut/pdf',null=True)
  def matche_file_type(cls, iname, ifile, request):
          # the extensions that lectut will recognise for the uploaded pdf
          ext = os.path.splitext(iname)[1].lower()
          return ext in ['.pdf']
'''
class Activity(models.Model):
  content_type=models.ForeignKey(ContentType, related_name='lectut')
  object_id=models.PositiveIntegerField()
  Upload = generic.GenericForeignKey('content_type','object_id')

  '''def create_upload(sender, instance, *args, **kwargs):
      if kwargs['created']:
               sku = u'%s%s%s' % ()
               u = Upload()
               u.save()

  post_save.connect(create_upload, sender=BaseUpload)



class Notification(models.Model):
  pub_date = models.DateTimeField('date published')
  ping=models.ForeignKey(prof)

  def save(self):
       "Get last value of serial_num from database, and increment before save"
       top = notification.objects.order_by('-serial_num')[0]
       self.serial_num = serial_num + 1
       super(notification, self).save()'''
