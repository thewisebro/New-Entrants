#!/usr/bin/python
import os, sys
sys.path.append(os.getcwd())
try:
  from apache import override as settings
except:
  import settings
#from django.core.management import setup_environ
#setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import time as ptime
from BeautifulSoup import BeautifulSoup
from notices.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from notices.utils import *

PeopleProxyUrl = "http://people.iitr.ernet.in/"

def notice_dict_for_email(notice):
  return {
    'subject' : notice.subject,
    'id' : notice.id,
    'content' : email_html_parser(notice.content),
  }

def get_subject_content(notice):
  subject = notice.subject
  content = render_to_string('notices/email.html',{'PeopleProxyUrl':PeopleProxyUrl,'notice':notice_dict_for_email(notice)})
  return subject,content

if __name__ == '__main__':
  notices = Notice.objects.filter(emailsend=False)
  for notice in notices:
    notice.emailsend = True
    notice.save()
    notice_users = notice.uploader.category.noticeuser_set.all()
    subject,content = get_subject_content(notice)
    email_ids = []
    for notice_user in notice_users:
      if notice_user.subscribed:
        email_ids.append(notice_user.user.email)
    while email_ids:
      first_100_email_ids = email_ids[:100]
      email_ids = email_ids[100:]
      try:
        msg = EmailMessage(subject,content,'eNotice',first_100_email_ids)
        msg.content_subtype = "html"
        msg.send()
      except Exception as e:
        print "Exception",e
      ptime.sleep(30)
