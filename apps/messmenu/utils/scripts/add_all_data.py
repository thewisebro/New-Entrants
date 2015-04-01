#!/usr/bin/env
import os, sys
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'channel-i.settings'
import settings
from django.core.management import setup_environ
setup_environ(settings)


# python imports
import datetime

# django imports
from messmenu.models import Menu
from api.model_constants import BHAWAN_CHOICES

# local imports
from messmenu.utils.utils import get_monday_date

def index():
  bhawans = dict(BHAWAN_CHOICES)
  print len(bhawans)
  for bhawan in bhawans:
    for week in range(-2, 3):
      monday_date = get_monday_date(week)
      for days in range(0, 7):
        date = monday_date + datetime.timedelta(days = days)
        for time_of_day in range(1,4):
          print bhawan, date, time_of_day
          menu = Menu(bhawan = bhawan, date = date, time_of_day = time_of_day)
          menu.save()

if __name__ == '__main__':
  index()
