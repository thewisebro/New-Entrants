# python imports
import datetime
import logging, traceback

# models
from messmenu.models import Menu


## returns date of monday of the requested week
def get_monday_date(week):
  current_date = datetime.date.today()
  date = current_date + datetime.timedelta(weeks = week)
  day_of_week = date.weekday()
  date -= datetime.timedelta(days = day_of_week)
  return date

def get_person(user):
  logger = logging.getLogger(__name__)
  groups = user.groups
  try:
    if groups.filter(name='Student').exists():
      user.person.designation = 'student'
    elif groups.filter(name='Faculty').exists():
      user.person = user.faculty
      user.person.designation = 'faculty'
      user.person.bhawan = None
    else:
      raise
    return user.person
  except:
    print traceback.format_exc()
    logger.error(traceback.format_exc())
    raise

def is_menu_filled(week):
  logger = logging.getLogger(__name__)
  date = get_monday_date(week)
  menu = Menu.objects.filter(bhawan='RVB', 
                      date__range = [date, date + datetime.timedelta(days = 6)]).\
                      exclude(content = '')
  count = Menu.objects.filter(bhawan='RVB', 
                      date__range = [date, date + datetime.timedelta(days = 6)]).\
                      exclude(content = '').count()
  if count:
    return True
  else:
    return False

