from django.core.exceptions import ValidationError
from django.db.models import Q

from core import models
from nucleus.models import User
from api import model_constants as MC
from events.constants import *
from groups.models import Group
from datetime import datetime, date, time, timedelta

class Calendar(models.Model):
  """ name : username of student,faculty,other in case of Private Calendar
             username of student_group's user in case of Group Calendar
             Appropriate name in case of Public Calendar

      users: Users who can upload events in this calendar.
             Mutiple users are used because of Public Calendar and Group Calendar

      In future, 'sharing calendar' functionality can be achieved for Private Calendars, without changes in model.
      In this case users would be those a calendar is shared with.They can upload and see the events.
  """
  name = models.CharField(max_length=MC.TEXT_LENGTH, unique=True)
  users = models.ManyToManyField(User)
  cal_type = models.CharField(max_length=MC.CODE_LENGTH, choices=CAL_TYPE_CHOICES)

  def __unicode__(self):
    if self.cal_type == 'PRI':
      return 'Personal Calendar'
    elif self.cal_type == 'PUB':
      return self.name + ' Calendar'
    elif self.cal_type == 'GRP':
      return Group.objects.get(user__username=self.name).name
    return self.name

  def shown_calendar_name(self):
    if self.cal_type == 'PRI':
      return 'Personal Calendar'
    if self.cal_type == 'PUB':
      return self.name + ' Calendar'
    if self.cal_type == 'GRP':
      return 'Groups Calendar'

class Event(models.Model):
  calendar = models.ForeignKey(Calendar)
  uploader = models.ForeignKey(User)
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  date = models.DateField()
  time = models.TimeField(blank=True, null=True)
  upto_date = models.DateField(blank=True, null=True)
  upto_time = models.TimeField(blank=True, null=True)
  place = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, verbose_name='Venue')
  description = models.CKEditorField(blank=True)
  event_type = models.CharField(max_length=MC.CODE_LENGTH, choices=EVENT_TYPE_CHOICES)
  datetime_added = models.DateTimeField(auto_now_add=True)
  email_sent = models.BooleanField(default=False)

  class Meta:
    ordering =['date', 'time']

  def __unicode__(self):
    return self.title

  def clean(self):
    if not ((self.date and self.date >= date.today()) or (self.upto_date and self.upto_date >= date.today())):
      raise ValidationError("Please enter today's date or upcoming date.")
    if self.upto_date and self.date:
      upto_dt = datetime.combine(self.upto_date, self.upto_time if self.upto_time else time())
      dt = datetime.combine(self.date, self.time if self.time else time())
      td = upto_dt - dt
      if td < timedelta():
        raise ValidationError("Upto date and time should be greater than event's starting date and time.")
    return super(Event, self).clean()

  def added_by(self):
    if self.calendar.cal_type == 'GRP':
      group = Group.objects.get(user__username = self.calendar.name)
      return group.user.html_name
    else:
      return ''

  @property
  def link(self):
    return "/#events/exact/"+str(self.pk)

  def duration(self):
    if self.upto_date:
      upto_dt = datetime.combine(self.upto_date,self.upto_time if self.upto_time else time())
      dt = datetime.combine(self.date,self.time if self.time else time())
      td = upto_dt - dt
      timedelta = str(td).split(', ')[-1]
      duration_str = ''
      if td.days > 0:
        duration_str += str(td.days)+(' Day' if td.days == 1 else ' Days')
      if timedelta != '0:00:00':
        hrs,mins = timedelta.split(':')[:2]
        if hrs == '0' and not td.days > 0:
          duration_str = mins+' Minutes'
        else:
          duration_str += (', '+hrs+(' Hour' if int(hrs)==1 else ' Hours')) if td.days > 0 else (hrs+(' Hour' if int(hrs)==1 else ' Hours'))
          if mins!= '00':
            duration_str += ', '+mins+' Minutes'
      elif td.days > 0:
        duration_str = str(td.days+1)+(' Day' if td.days == 1 else ' Days')
      return duration_str
    else:
      return ''


  def serialize(self):
    return {
      'title': self.title,
      'shown_calendar_name': self.calendar.shown_calendar_name(),
      'added_by': self.added_by(),
      'date': str(int(self.date.strftime('%d')))+self.date.strftime(' %B, %Y'),
      'time': self.time.strftime('%I:%M %p') if self.time else '',
      'duration': self.duration(),
      'place': self.place,
      'description': self.description,
      'uploader': self.uploader,
      'link': self.link,
    }


class EventsUser(models.Model):
  user = models.OneToOneField(User)
  calendars = models.ManyToManyField(Calendar, blank=True)
  email_subscribed = models.BooleanField(default=True)

  def __unicode__(self):
    return self.user.username

  def subscribe_to_calendars(self):
    calendars = Calendar.objects.exclude(~Q(name=self.user.username), cal_type='PRI')
    self.calendars.add(*list(calendars))
