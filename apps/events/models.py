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

class Event(models.Model):
  calendar = models.ForeignKey(Calendar)
  uploader = models.ForeignKey(User)
  title = models.CharField(max_length=MC.TEXT_LENGTH)
  date = models.DateField()
  time = models.TimeField(blank=True, null=True)
  upto_date = models.DateField(blank=True, null=True)
  upto_time = models.TimeField(blank=True, null=True)
  tlace = models.CharField(max_length=MC.TEXT_LENGTH, blank=True, verbose_name='Venue')
  description = models.CKEditorField(blank=True)
  event_type = models.CharField(max_length=MC.CODE_LENGTH, choices=EVENT_TYPE_CHOICES)
  datetime_added = models.DateTimeField(auto_now_add=True)
  email_sent = models.BooleanField(default=False)

  class Meta:
    ordering =['date', 'time']

  def __unicode__(self):
    return self.title

  def clean(self):
    if self.date and self.date < date.today():
      raise ValidationError("Please enter today's date or upcoming date.")
    if self.upto_date and self.date:
      upto_dt = datetime.combine(self.upto_date, self.upto_time if self.upto_time else time())
      dt = datetime.combine(self.date, self.time if self.time else time())
      td = upto_dt - dt
      if td < timedelta():
        raise ValidationError("Upto date and time should be greater than event's starting date and time.")
    return super(Event, self).clean()

class EventsUser(models.Model):
  user = models.OneToOneField(User)
  calendars = models.ManyToManyField(Calendar, blank=True)
  email_subscribed = models.BooleanField(default=True)

  def __unicode__(self):
    return self.user.username

  def subscribe_to_calendars(self):
    calendars = Calendar.objects.exclude(~Q(name=self.user.username), cal_type='PRI')
    self.calendars.add(*list(calendars))
