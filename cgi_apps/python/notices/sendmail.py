#!/usr/bin/python
"""
This module sends emails of notices to all subscribed users 
according to their preferences.
"""

import sys
import os
import time

current_app_path=os.getcwd()
sys.path.append(current_app_path+"/modules")

import dbinfo
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from include import *
from constant import *

ChanneliUrl = "https://channeli.in/notices/"

def EmailContent(content,subject,reference,idee):
  return """
  <div style="min-height:36px;background:#1b6f81;color:#ffffff;border-top-left-radius:5px;border-top-right-radius:5px;">
    <table style="border-spacing:0px;width:100%"><tbody><tr>
      <td style="padding:12px 6px 6px 6px;font-size:13px;">
        <table style="border-spacing:0px;">
        <tbody style="color:#ffffff;font-size:14px;vertical-align:top">
        <tr>             
	   <td style="width:65px;"><b>Subject :</b></td>
	   <td style=""> """+subject+\
	   """
	   </td>
        </tr>
        </tbody> 
        </table>
      </td>
      <td style="width:100px;vertical-align:top">
        <a href='"""+ChanneliUrl+"""' style="text-decoration:none;color:#ffffff;" target="_blank">
          <img src='"""+PeopleProxyUrl+"""template/images/enotice.png' style="font-weight:bold;font-size:15px;color:#ffffff;" alt="eNotice"/>
	</a>  
      </td>
    </tr></tbody></table>
  </div>
  <div style="background:#f0f0f0;padding:12px;font-size:12px;">"""+content+\
  """
  </div>
  <div style="clear:both"></div>
  <div style="height:18px;background:#1b6f81;padding:8px 6px 6px 6px;font-size:13px;color:#ffffff;">
    <div style="padding-right:6px;border-right:1px solid #0f404b;float:left;">
      <a href='"""+ChanneliUrl+"""#content/"""+str(idee)+"""' style="text-decoration:none;color:#ffffff;" target="_blank">
        <b>Web Version</b>
      </a>	
    </div>  
    <div style="padding:0px 6px;float:left;">
      <a href="http://channeli.in/settings/email/" style="text-decoration:none;color:#ffffff;" target="_blank">
        <b> Change Preferences / Unsubscribe</b>
      </a>	
    </div>
    <div style="margin:-30px;float:right;width:153px">
      <a href="https://market.android.com/details?id=in.ernet.iitr.people" style="text-decoration:none;" target="_blank">
        <img src='"""+PeopleProxyUrl+"""template/images/android.png' style="color:#92B901;font-weight:bold;" alt="Android Notice-Board" title="Android Notice-Board"/>
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
          <img src='"""+PeopleProxyUrl+"""template/images/imglogo.png' style="font-family:verdana;font-size:30px;font-weight:bold;line-height:26px" alt="IMG"
	  title="Information Management Group"/>
        </a>
      </td> 
      </tr></tbody></table> 
    </div>
    <div style="height:14px;border-top:1px solid #1b6f81;padding-top:6px;font-size:11px;">
      Copyright &copy; """+str(current_year)+""". All Rights Reserved. 
      <a href="img.channeli.in" style="text-decoration:none;color:#ffffff;" target="_blank">
        Information Management Group
      </a>
    </div>
  </div>
  """

db=dbinfo.db_connect()
sender="eNotice"

stdnts=db.query("select * from student_preference;").dictresult()

result=db.query("select id,subject,sent_to,sent_from,re_edited,reference from notices where emailsend='no' order by id desc;")
rslt=result.dictresult()

for row in rslt:
  notice_result = db.query("select emailsend from notices where id="+str(row['id'])+";").dictresult()
  if len(notice_result) > 0 and notice_result[0]['emailsend'] == 'yes':
    continue
  db.query("update notices set emailsend='yes' where id="+str(row['id'])+";")
  tempfile="data/n"+str(row['id'])
  tempinput=open(tempfile,"r")
  read=tempinput.read()
  tempinput.close()

  sent_to=row['sent_to']
  catsubcats=sent_to.split('|')
  CatSubcats={}
  for catsubcat in catsubcats:
    cat,subcats=catsubcat.split(':')
    CatSubcats[cat]=subcats.split(',')

  email_ids =[]
  for stdnt in stdnts:
    sent_to=stdnt['sent_to']
    catsubcats=sent_to.split('|')
    _CatSubcats={}
    for catsubcat in catsubcats:
      if catsubcat:
        cat,subcats=catsubcat.split(':')
        _CatSubcats[cat]=subcats.split(',')
    found=False
    if row['sent_from'] == 'Placement Office':
      for _cat in _CatSubcats:
        if 'po' in _CatSubcats[_cat]:
          found=True
    else:
      for _cat in _CatSubcats.keys():
        if _cat in CatSubcats.keys():
          _subcats=_CatSubcats[_cat]
          for _subcat in _subcats:
            if _subcat in CatSubcats[_cat]:
              found=True
              break
    if found == True:
      email_ids.append(stdnt['email_id'])

  eContent = EmailContent( read, row['subject'], row['reference'],row['id'])
  part = MIMEBase('text','html')
  part.set_payload(eContent)
  Encoders.encode_base64(part)
  msg = MIMEMultipart()
  msg['From'] = sender
  msg['To'] = 'NoticeBoardSubscribers'
  msg['Precedence'] = 'bulk'
  notice_subject = row['subject'].replace('&amp;','&')
  if row['re_edited'] == 'yes':
     msg['Subject'] = row['sent_from'] + " : (Notice changed)  " + notice_subject
  else:
     msg['Subject'] = row['sent_from'] + " : " + notice_subject
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
