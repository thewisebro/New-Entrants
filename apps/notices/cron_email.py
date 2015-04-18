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
#from include import *
#from constant import *

PeopleProxyUrl = "http://people.iitr.ernet.in/"

def EmailContent(content,subject,id1):
  content = email_html_parser(content)
  return """
    <div style="min-height:36px;background:#1b6f81;color:#ffffff;border-top-left-radius:5px;border-top-right-radius:5px;">
    <table style="border-spacing:0px;width:100%"><tbody><tr>
    <td style="padding:12px 6px 6px 6px;font-size:13px;">
    <table style="border-spacing:0px;">
    <tbody style="color:#ffffff;font-size:14px;vertical-align:top">
    <tr>             
    <td style="width:65px;"><b>Subject :</b></td>
    <td style=""> """ + subject +\
    """
    </td>
    </tr>
    </tbody> 
    </table>
    </td>
    <td style="width:100px;vertical-align:top">
    <a href= '""" + PeopleProxyUrl + """notices/' style="text-decoration:none;color:#ffffff;" target="_blank">
    <img src='""" +  PeopleProxyUrl + """media/notices/template/images/enotice.png' style="font-weight:bold;font-size:15px;color:#ffffff;" alt="eNotice"/>
    </a>  
    </td>
    </tr></tbody></table>
    </div>
    <div style="background:#f0f0f0;padding:12px;font-size:12px;"></div>""" + content +\
    """
    </div>
    <div style="clear:both"></div>
    <div style="height:18px;background:#1b6f81;padding:8px 6px 6px 6px;font-size:13px;color:#ffffff;">
    <div style="padding-right:6px;border-right:1px solid #0f404b;float:left;">
    <a href='""" +  PeopleProxyUrl + """/notices/content/""" + id1 + """' style="text-decoration:none;color:#ffffff;" target="_blank">
    <b>Web Version</b>
    </a>  
    </div>  
    <div style="padding:0px 6px;float:left;">
    <a href="channeli.in#settings/email" style="text-decoration:none;color:#ffffff;" target="_blank">
    <b> Change Preferences / Unsubscribe</b>
    </a>  
    </div>
    <div style="margin:-30px;float:right;width:153px">
    <a href="https://market.android.com/details?id=in.ernet.iitr.people" style="text-decoration:none;" target="_blank">
    <img src='""" +  PeopleProxyUrl + """/media/notices/template/images/android.png' istyle="color:#92B901;font-weight:bold;" alt="Android Notice-Board" title="Android Notice-Board"/>
    </a>
    </div>  
    </div>
    <div style="padding:10px 6px;background:#0f404b;color:#ffffff;">
    <div style="height:70px;padding-bottom:6px;padding-top:16px;">
    <table style="border-spacing:0px;width:100%"><tbody style="color:#ffffff;font-size:13px;"><tr>
    <td style="vertical-align:top;">
    <div style="height:20px;">
    <b>Email :</b>
    <a href="mailto:img.iitr.img@gmail.com" style="color:#ffffff;text-decoration:none;" target="_blank">img.iitr.img@gmail.com</a>
    </div>
    <div style="height:20px;">
    <b>Phone :</b> 01332 - 284521
    </div>
    <div style="height:20px;padding-top:5px">
    <b>Like us on</b> 
    <a href="https://www.facebook.com/IMGIITRoorkee" style="margin-left:0px 5px;text-decoration:none" target="_blank">
    <span style="background:#3b5998;color:white;font:bold 13px sans-serif;margin:2px 0px;padding:1px 5px 2px 5px">facebook</span>
    </a>
    </div>
    </td>
    <td style="width:100px;vertical-align:top;">
    <b>POWERED BY</b>
    </td>
    <td style="width:78px;vertical-align:top">
    <a href="img.channeli.in" style="text-decoration:none;color:#ffffff;" target="_blank">
    <img src='""" + PeopleProxyUrl + """media/notices/template/images/imglogo.png' style="font-family:verdana;font-size:30px;font-weight:bold;line-height:26px" alt="IMG"
    title="Information Management Group"/>
    </a>
    </td> 
    </tr></tbody></table> 
    </div>
    <div style="height:14px;border-top:1px solid #1b6f81;padding-top:6px;font-size:11px;">
    Copyright &copy;""" +  str(datetime.today().year) + """. All Rights Reserved. 
    <a href="img.channeli.in" style="text-decoration:none;color:#ffffff;" target="_blank">
    Information Management Group
    </a>
    </div>
    </div>
  """

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
      try:
        eContent = EmailContent(notice.content, notice.subject, notice.id)
        part = MIMEBase('text','html')
        part.set_payload(eContent)
        Encoders.encode_base64(part)
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = 'NoticeBoardSubscribers'
        msg['Precedence'] = 'bulk'
        notice_subject = row['subject'].replace('&amp;','&')
        if notice.re_edited == True:
           msg['Subject'] = notice.uploader.category + " : (Notice changed)  " + notice_subject
        else:
           msg['Subject'] = notice.uploader.category + " : " + notice_subject
        msg.attach(part)

        while email_ids:
          first_100_email_ids = email_ids[:100]
          email_ids = email_ids[100:]
          try:
            server = smtplib.SMTP('192.168.180.11')
            server.set_debuglevel(1)
            server.sendmail(sender, first_100_email_ids, msg.as_string())
            server.quit()
            time.sleep(30)
          except Exception,e:
            pass
        #msg = EmailMessage(subject,content,'eNotice',first_100_email_ids)
        #msg.content_subtype = "html"
        #msg.send()
