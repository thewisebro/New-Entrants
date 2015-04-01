# python imports
import datetime
import logging, traceback

# django imports
from django.db import models
from django.db import transaction

# models
from django.contrib.auth.models import User

# local imports
from api import model_constants as MC
from nucleus.models import Student


class Menu(models.Model):
  bhawan = models.CharField(max_length=MC.CODE_LENGTH, 
                            choices=MC.BHAWAN_CHOICES)
  #week = models.IntegerField(default=0)
  date = models.DateField(default=datetime.date.today())
  time_of_day = models.IntegerField(default=0)
  content = models.CharField(max_length=200, null=True, blank=True, default='')
  sum_ratings = models.IntegerField(default=0)
  count_ratings = models.IntegerField(default=0)
  raters = models.CharField(max_length=1000, null=True, blank=True)

  map_time_of_day = {
    'breakfast': 1,
    'lunch': 2,
    'dinner': 3
  }
  class Meta:
    ordering = ('time_of_day', 'date', )

  @classmethod
  def save_menu(self, formArray, bhawan, date):
    logger = logging.getLogger(__name__)
    with transaction.commit_on_success():
      for day in range(7):
        for time_of_day in range(1, 4):
          try:
            menu = Menu.objects.filter(bhawan = bhawan,
                              date = date + datetime.timedelta(days = day),
                              time_of_day = time_of_day)
            map(lambda x: x.delete(),menu)
            Menu.objects.create(bhawan = bhawan,
                              date = date + datetime.timedelta(days = day),
                              time_of_day = time_of_day,
                              content = formArray.get('content_%s_%s' % (day, time_of_day)))
          except:
            print traceback.format_exc()
            logger.error(traceback.format_exc())
            raise

class Feedback(models.Model):
  person = models.ForeignKey(Student,related_name='feedback_person')
  rating = models.IntegerField(default=0)
  date_created = models.DateTimeField(auto_now_add=True)
