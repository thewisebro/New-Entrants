from django.db import models
from nucleus.models import Student
# Create your models here.

class Course(models.Model):
  course_code = models.CharField(max_length = 100, primary_key = True)
  course_name = models.CharField(max_length = 200)
  def __unicode__(self):
    return self.course_code


class Bunk(models.Model):
  student = models.ForeignKey(Student,null=True)
  course_code = models.CharField(max_length = 100,default="xy")
  lec_bunk = models.IntegerField(default=0)
  lec_total = models.IntegerField(default=0)
  tut_bunk = models.IntegerField(default=0)
  tut_total = models.IntegerField(default=0)
  prac_bunk = models.IntegerField(default=0)
  prac_total = models.IntegerField(default=0)
  def __unicode__(self):
    return self.course_code


class TimeTable(models.Model):
  student = models.ForeignKey(Student,null=True)
  day = models.CharField(max_length=9)
  time = models.IntegerField(default=0)
  bunk = models.IntegerField(default=0)
  course_code = models.CharField(max_length=40,default="xy")
  course_name = models.CharField(max_length=40)
  class_type = models.IntegerField(default=0)
  def __unicode__(self):
    return self.student.user.username


