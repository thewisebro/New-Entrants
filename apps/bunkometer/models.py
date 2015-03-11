from django.db import models
from nucleus.models import Student
# Create your models here.

class Bunk(models.Model):
  rollNumber = models.CharField(max_length=15,default='13115100')
  subject = models.CharField(max_length=40)
  lec_bunk = models.IntegerField(default=0)
  tut_bunk = models.IntegerField(default=0)
  prac_bunk = models.IntegerField(default=0)
  def __unicode__(self):
    return self.rollNumber



class TimeTable(models.Model):
  rollNumber = models.CharField(max_length=15,default='13115100')
  day = models.CharField(max_length=9)
  time = models.TimeField()
  subject = models.CharField(max_length=40)
  class_type = models.CharField(max_length=3)
  def __unicode__(self):
    return self.rollNumber
