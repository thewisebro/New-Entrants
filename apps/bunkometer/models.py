from django.db import models
from nucleus.models import Student
# Create your models here.

class Bunk(models.Model):
  student = models.ForeignKey(Student, null=True)
  subject = models.CharField(max_length=40)
  lec_bunk = models.IntegerField(default=0)
  tut_bunk = models.IntegerField(default=0)
  prac_bunk = models.IntegerField(default=0)
  def __unicode__(self):
    return self.student



class TimeTable(models.Model):
  student = models.ForeignKey(Student, null=True)
  day = models.CharField(max_length=9)
  time = models.TimeField()
  subject = models.CharField(max_length=40)
  class_type = models.CharField(max_length=3)
  def __unicode__(self):
    return self.student
