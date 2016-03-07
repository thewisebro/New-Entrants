from core import models
from api import model_constants as MC
from nucleus.models import Faculty
from gate.constants import *

# Create your models here.

class Gate(models.Model):
  saved = models.BooleanField(default = False)
  declaration = models.BooleanField(default =False)
  prof = models.OneToOneField(Faculty)
  grade_pay = models.IntegerField(null=True,blank=True)
  pay_band_basic = models.IntegerField(null=True,blank=True)
  mobile_no = models.CharField(max_length=10, null=True, blank=True)
  phone_office = models.CharField(max_length=20,null=True,blank=True)
  phone_resi = models.CharField(max_length=20,null=True,blank=True)
  annual_income = models.IntegerField(null = True, blank = True)
  height = models.IntegerField(null=True, blank=True)
  weight = models.IntegerField(null=True, blank=True)
  age = models.IntegerField(null=True, blank=True)
  nominee_name = models.CharField(max_length=20, null=True, blank=True)
  relation_nominee = models.CharField(max_length=20, null=True, blank=True)
  date_of_join_position = models.CharField(max_length=20, null=True, blank=True)
  week_pref1 = models.CharField(max_length=50, choices=WEEKS, null=True, blank=True)
  week_pref2 = models.CharField(max_length =50, choices=WEEKS, null=True, blank=True)
  city_pref1 = models.CharField(max_length=50, choices=CITIES, null=True, blank=True)
  city_pref2 = models.CharField(max_length=50, choices=CITIES, null=True, blank=True)
  city_pref3 = models.CharField(max_length=50, choices=CITIES, null=True, blank=True)
  city_pref4 = models.CharField(max_length=50, choices=CITIES, null=True, blank=True)
  city_pref5 = models.CharField(max_length=50, choices=CITIES, null=True, blank=True)
  city_pref6 = models.CharField(max_length=50, choices=CITIES, null=True, blank=True)

  def __unicode__(self):
    return str(self.prof)
