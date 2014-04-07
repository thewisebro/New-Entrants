from core import models
from core import forms

from nucleus.models import User , Course , Faculty
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
  course=models.ForeignKey(Course, related_name='+')

  def __unicode__(self):
     return str(self.name)

class BaseUpload(models.Model):
  class Meta:
    abstract = True

  """def save(self, *args, **kwargs):
     if self.featured:
          self.__class__.objects.all().update(featured = False)
     super(Model, self).save(*args, **kwargs)"""

class UploadImage(BaseUpload):
  upload_image=models.ImageField(upload_to='lectut/images/')

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
class Upload(models.Model):
  content_type=models.ForeignKey(ContentType)
  object_id=models.PositiveIntegerField()
  lectutbatch=models.ForeignKey(LectutBatch)
  Upload = generic.GenericForeignKey('content_type','object_id')

  def create_upload(sender, instance, *args, **kwargs):
      if kwargs['created']:
               sku = u'%s%s%s' % ()
               u = Upload()
               u.save()

  post_save.connect(create_upload, sender=BaseUpload)


Act_Types = (
        ('tut' , 'Tutorial'),
        ('sol' , 'Solution'),
        ('que' , 'Question'),
        ('exm' , 'Exam Papers')
    )
class Activity(models.Model):
   log=models.ForeignKey(Upload)
   act_type=models.CharField(max_length=3 , choices=Act_Types)

   #Creates Activity when Upload model is created
   def create_activity(sender, instance, *args, **kwargs):
            if kwargs['created']:
                      sku = u'%s%s%s' % (instance.log)
                      s = Activity( log=instance)
                      s.save()

   post_save.connect(create_activity, sender=Upload)

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


