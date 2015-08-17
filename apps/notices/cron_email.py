#!/usr/bin/python
"""
This module sends emails of notices to all subscribed users 
according to their preferences.
"""

import sys
import os
import time

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from datetime import datetime
from notices.models import *
from BeautifulSoup import BeautifulSoup
from django.template.loader import render_to_string
#from include import *
#from constant import *

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

def email_html_parser(html):
  soup = BeautifulSoup(html)
  links = soup('a')
  for link in links:
    if link.has_key('href'):
      link['href'] = link['href'].replace(' ','%20')
      link_href_splits = link['href'].split('/')
      if link_href_splits[0] == '':
        link['href'] = PeopleProxyUrl+'media/notices/'+'/'.join(link_href_splits[3:])
  images = soup('img')
  for image in images:
    if image.has_key('src'):
      image['src'] = image['src'].replace(' ','%20')
  imgs = soup('img')
  for img in imgs:
    img_src_splits = img['src'].split('/')
    if img_src_splits[0] == '':
      img['src'] = PeopleProxyUrl+'media/notices/'+'/'.join(img_src_splits[3:])
  return str(soup)

def send_mails():
  sender="eNotice"
  notices = Notice.objects.filter(emailsend=False)
  for notice in notices:
    print notice
    notice.emailsend = True
    notice.save()
    print "emailsend=True set of notice with id : " + str(notice.id)
    notice_users = notice.uploader.category.noticeuser_set.all().filter(subscribed=True)
    subject,content = get_subject_content(notice)
    email_ids = []
    for notice_user in notice_users:
      print notice_user
      if notice_user.subscribed:
        print notice_user.user.email
        email_ids.append(notice_user.user.email)
    while email_ids:
      first_100_email_ids = email_ids[:100]
      email_ids = email_ids[100:]
      print first_100_email_ids
      part = MIMEBase('text','html')
      part.set_payload(content)
      Encoders.encode_base64(part)
      msg = MIMEMultipart()
      msg['From'] = sender
      msg['To'] = 'NoticeBoardSubscribers'
      msg['Precedence'] = 'bulk'
      notice_subject = notice.subject.replace('&amp;','&')
      if notice.re_edited == True:
         msg['Subject'] = notice.uploader.category.name + " : (Notice changed)  " + notice_subject
      else:
         msg['Subject'] = notice.uploader.category.name + " : " + notice_subject
      msg.attach(part)
      print "here1"
      try:
	  print "here1"
	  server = smtplib.SMTP('192.168.180.11')
	  server.set_debuglevel(1)
	  server.sendmail(sender, first_100_email_ids, msg.as_string())
	  server.quit()
	  print "sent"
      except Exception,e:
	  print "not sent"
	  pass
