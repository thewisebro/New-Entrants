#!/usr/bin/python
import os, sys
sys.path.append(os.getcwd())
try:
  from apache import override as settings
except:
  import settings
from django.core.management import setup_environ
setup_environ(settings)

import time as ptime
from BeautifulSoup import BeautifulSoup
from utilities.models import EmailAuthUser
from notices.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

PeopleProxyUrl = "http://people.iitr.ernet.in/"

def parse_html(html):
  soup = BeautifulSoup(html)
  links = soup('a')
  for link in links:
    if link.has_key('href'):
      link['href'] = link['href'].replace(' ','%20')
      link_href_splits = link['href'].split('/')
      if link_href_splits[0] == '':
        link['href'] = PeopleProxyUrl+'media_notices/'+'/'.join(link_href_splits[3:])
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
      img['src'] = PeopleProxyUrl+'media_notices/'+'/'.join(img_src_splits[3:])
  return str(soup)

def notice_dict_for_email(notice):
  return {
    'subject' : notice.subject,
    'id' : notice.id,
    'content' : parse_html(notice.content),
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
