#!/usr/bin/env
import os, sys
sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'channel-i.settings'
try:
  from apache import override as settings
except:  
  import settings
from django.core.management import setup_environ
setup_environ(settings)


# python imports
import datetime
import logging, traceback
import pdb
from copy import deepcopy

# django imports
from messmenu.models import Menu
from api import model_constants as MC
from django.db.models import Min
from django.http import HttpResponse

# local imports
from messmenu.utils.utils import get_monday_date
from messmenu.constants import weeks_to_show

def index():
  logger = logging.getLogger(__name__)
  bhawans = dict(MC.BHAWAN_CHOICES)
  date = get_monday_date(-2)
  try:
    ## oldest date in the db-table
    date_min = Menu.objects.aggregate(Min('date'))['date__min']
    weeks_diff = (date - date_min).days / 7
    if weeks_diff == 0:
      return
    menu = Menu.objects.order_by('date', 'time_of_day', 'bhawan').all()
  except:
    logger.error(traceback.format_exc())
  else:
    counter = 0
    total_rows = len(menu)
    for row in menu:
      row.date = row.date + datetime.timedelta(weeks = weeks_diff)
      diff = date_min + datetime.timedelta(weeks = 2*weeks_to_show, days = 6) - row.date
      if diff.days >= 0:
        ## 3 as there are 3 meals every day - breakfast, lunch, dinner
        linked_row = deepcopy(menu[counter + (weeks_diff * 7 * len(bhawans) * 3)])
        row.content = linked_row.content
        row.sum_ratings = linked_row.sum_ratings
        row.count_ratings = linked_row.count_ratings
        row.raters = linked_row.raters
      else:
        row.content = ''
        row.sum_ratings = 0
        row.count_ratings = 0
        row.raters = ''
      try:
        row.save()
      except:
        logger.error(traceback.format_exc())
      counter = counter + 1
  return

if __name__ == '__main__':
  index()
