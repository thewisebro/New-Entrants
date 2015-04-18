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
      try:
        msg = EmailMessage(subject,content,'eNotice',first_100_email_ids)
        msg.content_subtype = "html"
        msg.send()
      except Exception as e:
        print "Exception",e
