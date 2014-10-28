from core import models
from core import forms

from nucleus.models import User , Course , Faculty , Batch
from threadedcomments.models import ThreadedComment

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save

from notifications.models import Notification

fs = FileSystemStorage(location='Uploads')

# Create your models here.
'''class LectutUser(models.Model):
  user=models.OneToOneField(User)

  def __unicode__(self):
      return str(self.user)

class LectutBatch(models.Model):
  name=models.CharField(max_length=5 , null=True)
  lectutuser=models.ManyToManyField(LectutUser)
  course=models.ForeignKey(Course)

  def __unicode__(self):
     return str(self.name)'''

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
class UploadFile(BaseUpload):
  upload_file=models.FileField(upload_to='lectut/images/')
  name=models.CharField(max_length=100 , null=False)
  file_type=models.CharField(max_length=10 , null=False)
  upload_type=models.CharField(max_length=3 , default='tut')
  privacy=models.BooleanField(default=False)      #false means visible to all
  upload_user=models.ForeignKey(User)
  batch=models.ForeignKey(Batch)

  def save(self, *args, **kwargs):
    uploadedFile = super(UploadFile , self).save(*args, **kwargs)
    currentBatch = Batch.objects.get(id = self.batch)
    students = currentBatch.students.all()
    notification.save_notification('lectut','The user' +self.upload_user+ 'uploaded a file','lectut/'+self.id+'/upload',students,self)
    return uploadFile

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
  batch = models.ForeignKey(Batch)
  user = models.ForeignKey(User)

  def __unicode__(self):
    return str(self.text)

class DownloadLog(models.Model):
  uploadfile = models.ForeignKey(UploadFile)
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


   #Creates Activity when Upload model is created
  def create_activity(sender, instance, *args, **kwargs):
            if kwargs['created']:
                      sku = u'%s%s%s' % (instance.log)
                      s = Activity( log=instance)
                      s.save()

  post_save.connect(create_activity, sender=Upload)'''

class FluentComments(models.Model):
  threaded_comments=models.ForeignKey(ThreadedComment)
  activity=models.ForeignKey(Activity)

'''class Notification(models.Model):
  pub_date = models.DateTimeField('date published')
  ping=models.ForeignKey(prof)

  def save(self):
       "Get last value of serial_num from database, and increment before save"
       top = notification.objects.order_by('-serial_num')[0]
       self.serial_num = serial_num + 1
       super(notification, self).save()'''

"""
| lectut_lectutbatch                     |
| lectut_lectutbatch_lectutuser          |
| lectut_lectutuser                      |
| lectut_upload                          |
| lostfound_founditems                   |
| lostfound_lostitems


class FileUpload(models.Model):
   file_id = models.BigIntegerField(primary_key=True)
   file_location = models.CharField(max_length=450)
   topic = models.CharField(max_length=450)
   timestamp = models.DateTimeField()
   year = models.CharField(max_length=45, blank=True)
   file_type_list = (
       ('EP', 'Exampaper'),
       ('Le', 'Lecture'),
       ('So', 'Solution'),
       )
   file_type = modelsCharField(max_lenght=1, choices=file_type_list)
   faculty = models.ForeignKey(Faculty)
   course = models.ForeignKey(Course)
"""

