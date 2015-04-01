from core import models
from api import model_constants as MC
from nucleus.models import Student
from mcm.constants import *

# Create your models here.

class McmPerson(models.Model):
  student = models.ForeignKey(Student)
  air=models.IntegerField()
  unfair_means=models.BooleanField(default=False)
  family_income=models.IntegerField()
  other_scholarship=models.BooleanField(default=False)
  date_time = models.DateTimeField()

class StudentLoanAid(models.Model):
  student = models.OneToOneField(Student)
  check = models.BooleanField(default = False)
  cgpa = models.CharField(max_length = 6, null = True, blank = True)
  sgpa = models.CharField(max_length = 6, null = True, blank = True)
  fathers_income = models.IntegerField(null = True, blank = True)
  fathers_pan_no = models.CharField(max_length = 10, null = True, blank = True)
  mothers_pan_no = models.CharField(max_length = 10, null = True, blank = True)
  gaurdians_pan_no = models.CharField(max_length = 10, null = True, blank = True)
  guardians_name = models.CharField(max_length = 20, null=True, blank = True)
  guardians_occupation = models.CharField(max_length = 20, null=True, blank = True)
  guardians_income = models.IntegerField(null=True, blank = True)
  guardians_address = models.CharField(max_length = 50, null=True, blank = True)
  mothers_occupation = models.CharField(max_length = 50, null=True, blank = True)
  mothers_income = models.IntegerField(null=True, blank = True)
  other_scholarship_details = models.CharField(max_length = 100, null=True, blank = True)
  previous_aid_amount = models.IntegerField(null=True, blank=True)
  previous_aid_session = models.CharField(max_length = 9, null=True, blank = True)
  work_bhawan_details = models.CharField(max_length = 50, null=True, blank = True )
  date_time = models.DateTimeField(null = True, blank = True)

class MCM(models.Model):
  student = models.OneToOneField(Student)
  scholar_type=models.CharField(max_length=10, choices=SCHOLAR_TYPE, null=True, blank= True)
  check = models.BooleanField(default = False)
  air=models.IntegerField(blank=True, null=True)
  unfair_means=models.BooleanField(default=False)
  cgpa = models.CharField(max_length = 6, null = True, blank = True)
  sgpa = models.CharField(max_length = 6, null = True, blank = True)
  family_income = models.IntegerField(null = True, blank = True)
  other_scholarship_details = models.CharField(max_length = 100, null=True, blank = True)
  datetime = models.DateTimeField(null=True, blank=True, auto_now=True)
  payment_choice=models.CharField(max_length=10, choices=PAYMENT_CHOICE, null= True, blank=True)

  def __unicode__(self):
    return str(self.student)
