import os
import logging
from datetime import datetime,time
import json as simplejson

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.html import escape
from django.db.models import Q
from django.template.loader import render_to_string
from django.conf import settings

from events.models import *
from groups.models import Group
from events.forms import EventFormGenerator
from filemanager import FileManager
from api.utils import dialog_login_required, ajax_login_required

logger = logging.getLogger('channel-i_logger')

def calendar_dict(calendar):
  if calendar.cal_type == 'PRI':
    return {'name':calendar.name,'verbose_name':'Personal'}
  if calendar.cal_type == 'PUB':
    return {'name':calendar.name,'verbose_name':calendar.name}
  if calendar.cal_type == 'GRP':
    return {'name':calendar.name,'verbose_name':Group.objects.get(user__username = calendar.name).name}

@dialog_login_required
def add(request):
  # form initiated to render media on template
  cal_type = 'GRP' if request.user.in_group('Student Group') else 'PRI'
  form = EventFormGenerator(Calendar.objects.get(name=request.user.username, cal_type=cal_type))()
  calendar = None
  calendars = Calendar.objects.filter(users__in = [request.user])
  if calendars.count() == 1:
    calendar = calendars[0]
  calendars = map(calendar_dict, calendars)
  if (request.method == 'POST' and calendar or\
      (request.POST.has_key('calendar_name') and request.POST['calendar_name'])):
    if not calendar:
      calendar = Calendar.objects.get(name = request.POST['calendar_name'])
    EventForm = EventFormGenerator(calendar)
    if calendar.users.filter(username = request.user.username).count() == 0:
      return HttpResponse('')
    if request.POST.has_key('submit'):
      form = EventForm(request.POST)
      if form.is_valid():
        event = form.save(commit=False)
        event.calendar = calendar
        event.uploader = request.user
        event.save()
        messages.success(request,'Event added successfully.')
        return HttpResponseRedirect(reverse('close_dialog', kwargs={
              'dialog_name': 'add_event_dialog'
        }))
    else:
      form = EventForm()
  return render(request, 'events/add.html', {
      'form':form,
      'calendars':calendars,
      'calendar':calendar
  })


@dialog_login_required
def edit(request,event_id):
  event = Event.objects.get(pk = event_id)
  if event.calendar.users.filter(username=request.user.username).count() == 0:
    return HttpResponse('')
  EventForm = EventFormGenerator(event.calendar, exclude_event_type=event.email_sent)
  form = EventForm(instance = event)
  if request.method == 'POST':
    form = EventForm(request.POST, instance=event)
    if form.is_valid():
      event = form.save(commit=False)
      event.uploader = request.user
      event.save()
      messages.success(request,'Event changed successfully.')
      return HttpResponseRedirect(reverse('close_dialog', kwargs={
              'dialog_name': 'edit_event_dialog'
      }))
  return render(request, 'events/edit.html', {
      'form':form,
  })

@ajax_login_required
def delete(request):
  if request.is_ajax() and request.method == 'POST':
    event_id = request.POST['id']
    try:
      event = Event.objects.get(pk = event_id)
    except Exception as e:
      print "Exception accured",e
    json = None
    if event.calendar.users.filter(username = request.user.username).count() == 1:
      event.delete()
      messages.success(request,'Event deleted successfully.')
      json = simplejson.dumps({'result':'success'})
    else:
      messages.error(request,'There was some error deleting the event')
      json = simplejson.dumps({'result':'failure'})
  return HttpResponse(json,content_type='application/json')

def get_calendars(request):
  if request.is_ajax() and request.method == 'GET':
    calendars = [{'name':'all','verbose_name':'All'}]
    public_calendars = Calendar.objects.filter(cal_type='PUB')
    calendars += map(lambda cal:{'name':cal.name,'verbose_name':cal.name},public_calendars)+\
                  [{'name':'groups','verbose_name':'Groups'}]
    if request.user.is_authenticated():
      user_calendar,created = Calendar.objects.get_or_create(name=request.user.username)
      if created:
        user_calendar.users.add(request.user)
        if request.user.in_group('Student Group'):
          user_calendar.cal_type = 'GRP'
        else:
          user_calendar.cal_type = 'PRI'
        user_calendar.save()
      if not request.user.in_group('Student Group'):
        calendars += [{'name':user_calendar.name,'verbose_name':'Personal'}]
    json = simplejson.dumps({'calendars':calendars})
    return HttpResponse(json, content_type='application/json')

def get_events_dates(request):
  if request.is_ajax() and request.method == 'GET':
    month = request.GET['month']
    year = request.GET['year']
    if request.user.is_authenticated():
      events = Event.objects.exclude(~Q(calendar__name = request.user.username),calendar__cal_type = 'PRI')
    else:
      events = Event.objects.exclude(calendar__cal_type = 'PRI')
    events = events.filter(date__month = month,date__year = year)
    dates = map(lambda e:e.date.day,events)
    json = simplejson.dumps({'dates':dates})
    return HttpResponse(json,content_type='application/json')

def added_by(event):
  if event.calendar.cal_type == 'GRP':
    group = Group.objects.get(user__username = event.calendar.name)
    return "<a href='/#groups/%s/'>"%group.user.username +\
           group.user.html_name+"</a>"
  else:
    return ''

def duration(event):
  if event.upto_date or event.upto_time:
    if event.upto_time and not event.upto_date:
      event.upto_date = event.date
    upto_dt = datetime.combine(event.upto_date,event.upto_time if event.upto_time else time())
    dt = datetime.combine(event.date,event.time if event.time else time())
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

def time_str(time):
  return time.strftime("%I:%M %p")

def date_str(date):
  return "%s %s" % (date.day, date.strftime("%b"))

def uptotime(event):
  if event.upto_time:
    if not event.upto_date:
      event.upto_date = event.date
    if event.upto_date == event.date:
      return "%s - %s" % (time_str(event.time),time_str(event.upto_time))
    else:
      return "%s %s - %s %s" % (date_str(event.date), time_str(event.time),
              date_str(event.upto_date), time_str(event.upto_time))
  elif event.upto_date:
      return "%s - %s" % (date_str(event.date), date_str(event.upto_date))
  elif event.time:
      return "%s" % (time_str(event.time),)
  else:
      return ''

def weekday(event):
  dif = (event.date-datetime.now().date()).days
  if dif == 0:
    return 'Today'
  if dif == 1:
    return 'Tomorrow'
  if 1 < dif < 7:
    return event.date.strftime("%A")
  return ''

def shown_calendar_name(calendar):
  if calendar.cal_type == 'PRI':
    return 'Personal Calendar'
  if calendar.cal_type == 'PUB':
    return calendar.name + ' Calendar'
  if calendar.cal_type == 'GRP':
    return 'Groups Calendar'

def diff(d1,d2):
  return (d1-d2.date()).days

def event_dict(event,user):
  return {
    'id' : event.pk,
    'calendar_name' : event.calendar.name,
    'shown_calendar_name' : shown_calendar_name(event.calendar),
    'title' : escape(event.title),
    'added_by' : added_by(event),
    'date' : 'Today' if diff(event.date,datetime.today())==0 \
             else ('Tomorrow' if diff(event.date,datetime.today()) == 1 else \
             str(int(event.date.strftime('%d')))+event.date.strftime(' %B, %Y')),
    'time' : event.time.strftime('%I:%M %p') if event.time else '',
    'uptotime' : uptotime(event),
    'datetime':(datetime.combine(event.date,event.time) if event.time else
                event.date).strftime('%Y-%m-%d %H:%M:%S'),
    'duration':duration(event),
    'day': event.date.day,
    'monthyear': event.date.strftime("%b, %y"),
    'place' : escape(event.place),
    'description' : event.description,
    'weekday': weekday(event),
    'editable': event.calendar.users.filter(username = user.username).count()
  }

def fetch(request):
  if request.is_ajax() and request.method == 'GET':
#    try:
      calendar_name = request.GET['calendar_name']
      group_name = None
      if request.GET.has_key('group_name'):
        group_name = request.GET['group_name']
      action = request.GET['action']
      pk = request.GET['id']
      number = int(request.GET['number'])
      by_month_year = request.GET['by_month_year']
      if request.user.is_authenticated():
        events = Event.objects.exclude(~Q(calendar__name=request.user.username), calendar__cal_type='PRI')
      else:
        events = Event.objects.exclude(calendar__cal_type='PRI')
      if calendar_name == 'all':
        pass
      elif calendar_name == 'groups':
        events = Event.objects.filter(calendar__cal_type='GRP')
        if group_name:
          events = events.filter(calendar__name=group_name)
      else:
        events = Event.objects.filter(calendar__name=calendar_name)
      if by_month_year:
        month = request.GET['month']
        year = request.GET['year']
        if action == 'first':
          events = events.filter(date__month = month,date__year=year)
        elif action == 'next':
          pk_event = Event.objects.get(pk=pk)
          pk_datetime = datetime.combine(pk_event.date,pk_event.time) if pk_event.time else pk_event.date
          events = events.extra(where=["IF(time,ADDTIME(date,time),date) > "+pk_datetime.strftime("'%Y-%m-%d %H:%M:%S'"),
              "MONTH(date) = "+month,"YEAR(date) = "+year])
      else:
        if action == 'first':
          events = events.filter(Q(date__gte = datetime.today()) | Q(upto_date__gte = datetime.today()))
        elif action == 'next':
          pk_event = Event.objects.get(pk=pk)
          pk_datetime = datetime.combine(pk_event.date,pk_event.time) if pk_event.time else pk_event.date
          events = events.extra(where=["IF(time,ADDTIME(date,time),date) > "+pk_datetime.strftime("'%Y-%m-%d %H:%M:%S'")])
      json = simplejson.dumps({'events':map(lambda e:event_dict(e,request.user),events[:number]),'more':int(events.count()>number)})
      return HttpResponse(json,content_type='application/json')
#    except Exception as e:
#      logger.exception('Exception accured in events/fetch : '+str(e))
#      return HttpResponse('')

@login_required
def browse(request,calendar_name,path):
  calendar = Calendar.objects.get(name = calendar_name)
  if calendar.users.filter(username = request.user.username).count() == 1:
    if not os.path.exists(settings.MEDIA_ROOT+'events/uploads/'+calendar.name):
      os.chdir(settings.MEDIA_ROOT+'events/uploads/')
      os.mkdir(calendar.name)
    fm = FileManager(basepath=settings.MEDIA_ROOT+'events/uploads/'+calendar.name,
        ckeditor_baseurl='/media/events/uploads/'+calendar.name,
        maxspace=50*1024, maxfilesize=5*1024)
    return fm.render(request,path)
