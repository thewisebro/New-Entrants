from django.db import models
from django.contrib.auth.models import User
from nucleus.models import *
from datetime import datetime
from crop_image import CropImage
from django.conf import settings
# Create your models here.

class MemberPhoto(CropImage):
  unique_name = 'genform_pic'
  field_name = 'pic'
  width = 132
  height = 150

  @classmethod
  def get_instance(cls, request, pk):
    return request.user.student.pic

  @classmethod
  def get_image_url(cls, image_field):
    if image_field:
      return image_field.instance.pic.url
    else:
      return settings.STATIC_URL + 'images/nucleus/default_dp.png'

  @classmethod
  def file_name(cls, image_field, fname):
    if image_field.instance.pic:
      url_image = image_field.instance.pic.url
    else:
      url_image = "genform/pics/" + image_field.instance.person.user.username + "_1.jpg"
    previous_name = url_image.split(".")[0]
    prev_name = previous_name.split("/")[-1]
    if "_" in prev_name:
      new_number = str(int(prev_name.split("_")[-1]) + 1)
    else:
      new_number = "1"
    fname = image_field.instance.person.user.username + '_' + new_number + '.' +fname.split('.')[-1]
    return fname

class LibForm(models.Model):
  person = models.OneToOneField(Student, null=False, blank=False)
  birth_date = models.DateField(blank=False)
  blood_group = models.CharField(max_length=3, choices=MC.BLOOD_GROUP_CHOICES, blank=False, verbose_name="Blood Group")
  personal_contact_no = models.CharField(max_length=12, blank=False, verbose_name="Mobile No. (Self)")
  pincode = models.CharField(max_length=10, blank=False)
  permanent_address = models.CharField(max_length=100, blank=False, verbose_name="Permanent Address")
  fathers_or_guardians_name = models.CharField(max_length=100, blank=False, verbose_name="Father's /Guardians's Name")
  home_parent_guardian_phone_no = models.CharField(max_length=12, blank=False, verbose_name="Home /Parent's /Local Guardian's Phone No.")
  valid_till = models.DateField(blank=False)
  reason = models.CharField(max_length=100, blank=False)

  def __unicode__(self):
    return str(self.person)

class Pic(models.Model):
  person = models.OneToOneField(Student, primary_key=True)
  pic =  MemberPhoto.ModelField(
                           upload_to = 'genform/pics/',
                           blank = True,
                           null = True,
          )
