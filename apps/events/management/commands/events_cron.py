from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from django.conf import settings
import time as ptime
from BeautifulSoup import BeautifulSoup
from events.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from events.views import duration,shown_calendar_name

PeopleProxyUrl = "http://people.iitr.ernet.in/"

def parse_html(html):
  soup = BeautifulSoup(html)
  links = soup('a')
  for link in links:
    if link.has_key('href'):
      link['href'] = link['href'].replace(' ','%20')
      link_href_splits = link['href'].split('/')
      if link_href_splits[0] == '':
        link['href'] = PeopleProxyUrl+'media_events/'+'/'.join(link_href_splits[3:])
  images = soup('img')
  for image in images:
    if image.has_key('src'):
      image['src'] = image['src'].replace(' ','%20')
  first = soup.first()
  if first.name == 'p':
    first['style'] = (first['style']+';' if first.has_key('style') else '') + 'margin:0px'
  imgs = soup('img')
  for img in imgs:
    if img.has_key('style'):
      css_properties = img['style'].split(';')
      new_css_properties = []
      for css_property in css_properties:
        splits = css_property.split(':')
        if not (len(splits) == 2 and (splits[0].replace(' ','') == 'min-height' or splits[0].replace(' ','') == 'height')):
          new_css_properties.append(css_property)
      img['style'] = ';'.join(new_css_properties)
    img['style'] = (img['style']+';' if img.has_key('style') else '') + 'max-width:670px;height:auto'
    img_src_splits = img['src'].split('/')
    if img_src_splits[0] == '':
      img['src'] = PeopleProxyUrl+'media_events/'+'/'.join(img_src_splits[3:])
  return str(soup)

def added_by(event):
  if event.calendar.cal_type == 'GRP':
    group = Group.objects.get(user__username = event.calendar.name)
    return group.user.html_name
  else:
    return ''

def event_dict_for_email(event):
  return {
    'title' : event.title,
    'shown_calendar_name' : shown_calendar_name(event.calendar)+' Calendar',
    'added_by' : added_by(event),
    'date' : str(int(event.date.strftime('%d')))+event.date.strftime(' %B, %Y'),
    'time' : event.time.strftime('%I:%M %p') if event.time else '',
    'duration':duration(event),
    'place' : event.place,
    'description' : parse_html(event.description),
  }

def get_subject_content(event):
  subject = event.title
  content = render_to_string('events/email.html',{'PeopleProxyUrl':PeopleProxyUrl,'event':event_dict_for_email(event)})
  return subject,content

class Command(BaseCommand):
  args = ''
  help = 'Generates cached pages for production'

  def handle(self, *args, **options):
    events = Event.objects.extra(
      where = [
        "NOT event_type = 'NOEMAIL'",
        "email_sent = 0",
        "NOT ((event_type = 'REMINDER') AND (DATE_ADD(NOW(),INTERVAL 6 HOUR) < IF(time,ADDTIME(date,time),date)))"]
    )
    for event in events:
      event.email_sent = True
      event.save()
      event_users = event.calendar.eventsuser_set.all()
      subject,content = get_subject_content(event)
      email_ids = []
      for event_user in event_users:
        if event_user.email_subscribed:
          # dont send event mails to passout students
          try:
            if not event_user.user.student.passout_year:
              email_ids.append(event_user.user.email)
          except:
            email_ids.append(event_user.user.email)
      while email_ids:
        first_100_email_ids = email_ids[:100]
        email_ids = email_ids[100:]
        try:
          msg = EmailMessage(subject,content,'Event',first_100_email_ids)
          msg.content_subtype = "html"
          msg.send()
        except Exception as e:
          print "Exception",e
        ptime.sleep(30)
