from core import models
from core import forms

from nucleus.models import User , Course , Faculty , Batch
from threadedcomments.models import ThreadedComment

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save

fs = FileSystemStorage(location='Uploads')

# Create your models here.
class LectutUser(models.Model):
  user=models.OneToOneField(User)

  def __unicode__(self):
      return str(self.user)

class LectutBatch(models.Model):
  name=models.CharField(max_length=5 , null=True)
  lectutuser=models.ManyToManyField(LectutUser)
  course=models.ForeignKey(Course)

  def __unicode__(self):
     return str(self.name)

class TextNotice(models.Model):
  text=models.CharField(max_length=500 , null=False)
  upload_user=models.ForeignKey(User)
  batch=models.ForeignKey(Batch)

  def __unicode__(self):
    return str(self.text)

class BaseUpload(models.Model):
  class Meta:
    abstract = True

  """def save(self, *args, **kwargs):
     if self.featured:
          self.__class__.objects.all().update(featured = False)
     super(Model, self).save(*args, **kwargs)"""

Act_Types = (
            ('lec' , 'Lecture'),
            ('tut' , 'Tutorial'),
            ('sol' , 'Solution'),
            ('que' , 'Question'),
            ('exm' , 'Exam Papers')
            )

class UploadFile(BaseUpload):
  upload_file=models.FileField(upload_to='lectut/images/')
  name=models.CharField(max_length=100 , null=False)
  file_type=models.CharField(max_length=10 , null=False)
  upload_type=models.CharField(max_length=3 , choices=Act_Types , default='tut')
  privacy=models.BooleanField(default=False)      #false means visible to all
  upload_user=models.ForeignKey(User)
  batch=models.ForeignKey(Batch)

  def __unicode__(self):
    return str(self.upload_file)

class DownloadLog(models.Model):
  uploadfile = models.ForeignKey(UploadFile)
  user = models.ForeignKey(User)

  def __unicode__(self):
    return self.id
'''class UploadVideo(BaseUpload):
  upload_video=models.FileField(upload_to='lectut/videos' , null=True)
  def matche_file_type(cls, iname, ifile, request):
        # the extensions that lectut will recognise for the uploaded video
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv',]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

class UploadPPT(BaseUpload):
  upload_ppt=models.FileField(upload_to='lectut/ppts', null=True)
  def matche_file_type(cls, iname, ifile, request):
        # the extensions that lectut will recognise for the uploaded ppt
        ext = os.path.splitext(iname)[1].lower()
        return ext in ['.ppt']

class UploadPdf(BaseUpload):
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

  def __init__(self):
    return self.object_id
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


