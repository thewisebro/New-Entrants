#!/usr/bin/python
"""
This module sends emails of notices to all subscribed users 
according to their preferences.
"""

import sys
import os

current_app_path=os.getcwd()
sys.path.append(current_app_path+"/modules")

import dbinfo
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from include import *
from constant import *

PeopleProxyUrl = "http://people.iitr.ernet.in/Notices/"

IMG_div = """
<div style="height:100px;width:600px;border-radius:3px;border:1px solid #bbb">
 <div style="height:84px;width:450px;margin:8px 10px;float:left">
  <span style="font:bold 14px sans-serif">Powered by IMG ( 
   <a style="color:#333" target="_blank" 
    href="http://www.iitr.ac.in/campus_life/pages/Groups_and_Societies+IMG.html">Information Management Group</a> )
  </span>
  <br>
  <span style="font:13px  sans-serif">
   Contact us @
   <br>
   Email : <a href="mailto:img.iitr.img@gmail.com" style="color:#333">img.iitr.img@gmail.com</a>
   <br>
   Phone No : 4521
   <br>
   LIKE us on 
   <a href="https://www.facebook.com/IMGIITRoorkee" style="margin-left:0px 5px;text-decoration:none" target="_blank">
    <span style="background:#3b5998;color:white;font:bold 13px sans-serif;margin:2px 0px;padding:0px 5px">Facebook</span>
   </a>

   <a style="margin-left:20px;text-decoration:none;color:green;font-style:italic;font-weight:bold" target="_blank"
    onmouseover="this.style.textDecoration='underline'" onmouseout="this.style.textDecoration='none'"
    href="https://market.android.com/details?id=in.ernet.iitr.people"
   >*Notice Board now on android</a>

  </span>
 </div>
 <div style="height:100px;width:100px;margin:0px 5px;float:right">
  <a target="_blank" href="http://www.iitr.ac.in/campus_life/pages/Groups_and_Societies+IMG.html">
   <img src=\"""" + PeopleProxyUrl + """template/images/img_logo.png\" width="100%"></img>
  </a>
 </div>
</div>
"""

def EmailContent(content,subject,reference,key,idee):
    upper = "<div style=\"margin:0px;padding:5px;background:#a0a0ff\">\
            <div style=\"margin:0px;padding:0px;width:70%;float:left\"><b>Subject : </b> "+subject+"</div>\
            <div style=\"margin:0px;padding:0px;width:28%;float:right\"><b>Reference No. : </b>"+reference+"</div>\
	    <div style=\"clear:both\"></div></div>"

    middle = "<div style=\"margin:0px;padding:0px 5px\">"+content+"</div><br>\
              Having problems in viewing mail? <a href=\""+PeopleProxyUrl+"?id="+str(idee)+"\">View in browser</a>."

    unsubscribe_link = "<br>It's an automatic generated mail ; Don't reply .<br><a href=\""+PeopleProxyUrl+"unsubscribe.cgi?key="+\
                        key+"\" target=\"_blank\">Unsubscribe</a> from Notice-Board<br><br>"

    return upper + middle + unsubscribe_link + IMG_div



totalsend = 0
server = smtplib.SMTP('192.168.121.26')
server.set_debuglevel(1)
db=dbinfo.db_connect()
sender="eNotice@Notice-Board"

stdnts=db.query("select * from student_preference;").dictresult()

result=db.query("select id,subject,sent_to,sent_from,re_edited,reference from notices where emailsend='no' order by id desc;")
rslt=result.dictresult()

for row in rslt:
	db.query("update notices set emailsend='yes' where id="+str(row['id'])+";")
	tempfile="data/n"+str(row['id'])
	tempinput=open(tempfile,"r")
	read=correct_urls(tempinput.read())
	tempinput.close()
	
	sent_to=row['sent_to']
	catsubcats=sent_to.split('|')
	CatSubcats={}
	for catsubcat in catsubcats:
		cat,subcats=catsubcat.split(':')
		CatSubcats[cat]=subcats.split(',')
 
	for stdnt in stdnts:
		sent_to=stdnt['sent_to']
		catsubcats=sent_to.split('|')
		_CatSubcats={}
		for catsubcat in catsubcats:
			cat,subcats=catsubcat.split(':')
			_CatSubcats[cat]=subcats.split(',')
  		found=False
		for _cat in _CatSubcats.keys():
			if _cat in CatSubcats.keys():
				_subcats=_CatSubcats[_cat]
				for _subcat in _subcats:
					if _subcat in CatSubcats[_cat]:
						found=True
						break
		if found == True:
			eContent = EmailContent( read, row['subject'], row['reference'],stdnt['key'],row['id']) 
			part = MIMEBase('text','html')
			part.set_payload(eContent)
			Encoders.encode_base64(part)
			msg = MIMEMultipart()
			msg['From'] = sender
			msg['To'] = stdnt['email_id']
			notice_subject = row['subject'].replace('&amp;','&')
			if row['re_edited'] == 'yes':
			   msg['Subject'] = row['sent_from'] + " : (Notice changed)  " + notice_subject  
			else:
			   msg['Subject'] = row['sent_from'] + " : " + notice_subject
			msg.attach(part)	
			try:
			  server.sendmail(sender,stdnt['email_id'], msg.as_string())
		        except Exception,e:
			  pass
			totalsend+=1			
        print totalsend
        if row['sent_from'] in ['DOSW IITR']:
		regol_db = dbinfo.regol_db_connect()
		persons = regol_db.query("SELECT person_id FROM person;").dictresult()
                for person in persons:
			eContent = EmailContent( read, row['subject'], row['reference'],stdnt['key'],row['id']) 
			part = MIMEBase('text','html')
			part.set_payload(eContent)
			Encoders.encode_base64(part)
			msg = MIMEMultipart()
			msg['From'] = sender
			msg['To'] = person['person_id']+'@iitr.ernet.in'
			notice_subject = row['subject'].replace('&amp;','&')
			if row['re_edited'] == 'yes':
			   msg['Subject'] = row['sent_from'] + " : (Notice changed)  " + notice_subject  
			else:
			   msg['Subject'] = row['sent_from'] + " : " + notice_subject
			msg.attach(part)	
			try:
			  server.sendmail(sender,stdnt['email_id'], msg.as_string())
		        except Exception,e:
			  pass		        
server.quit()
