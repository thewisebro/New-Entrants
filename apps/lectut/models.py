from core import models
from core import forms
from nucleus.models import User , Course , Faculty
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='Uploads')

# Create your models here.
class Lectut_User(models.Model):
  user=models.ForeignKey(User)

class Lectut_Course(models.Model):
  course=models.ForeignKey(Course)

class Batch(models.Model):
  name=models.CharField(max_length=20)
  student=models.ManyToManyField(Lectut_User)
  lectut_course=models.ForeignKey(Lectut_Course)

class Upload_Image(models.Model):
  upload_image=models.ImageField(upload_to='../../media/lectut/images')

class Video(models.Model):
  upload_video=models.FileField(upload_to='../../media/lectut/videos' , null=True)
  def matche_file_type(cls, iname, ifile, request):
        # the extensions that lectut will recognise for the uploaded video
        filename_extensions = ['.dv', '.mov', '.mp4', '.avi', '.wmv',]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

class Ppt(models.Model):
  upload_ppt=models.FileField(upload_to='../../media/lectut/ppts', null=True)
  def matche_file_type(cls, iname, ifile, request):
        # the extensions that lectut will recognise for the uploaded ppt
        ext = os.path.splitext(iname)[1].lower()
        return ext in ['.ppt']

class Pdf(models.Model):
  upload_pdf=models.FileField(upload_to='../../media/lectut/pdf',null=True)
  def matche_file_type(cls, iname, ifile, request):
          # the extensions that lectut will recognise for the uploaded pdf
          ext = os.path.splitext(iname)[1].lower()
          return ext in ['.pdf']

class Upload(models.Model):
  Upload = generic.GenericForeignKey('upload_image','upload_video','upload_ppt')

class lectut_Faculty(models.Model):
  faculty=models.ForeignKey(Faculty)

'''class Notification(models.Model):
  pub_date = models.DateTimeField('date published')
  ping=models.ForeignKey(prof)

  def save(self):
       "Get last value of serial_num from database, and increment before save"
       top = notification.objects.order_by('-serial_num')[0]
       self.serial_num = serial_num + 1
       super(notification, self).save()'''


