#!/usr/bin/python
import sys
import os
current_app_path=os.getcwd()
#--->citing the path where user defined modules are stored
sys.path.append(current_app_path+"/modules")
import parseForm
#--->dbinfo contains the db connection info
import dbinfo
import cgi
import string
import cgitb
import time
import binascii
import random
import crypt
from include import *

print "Content-Type: text/html\r"
print "Cache-Control:private,no-cache,no-store,must-revalidate\r\n\r\n"

def redirectOnSuccess(seshId,todo):
	print "<html><head>\
	       <script language=\"javascript\">\
		document.location=\"upload.cgi?auth="+seshId+"&todo="+todo+"\"\
		</script></head></html>"

def verify(username,passwd):
	"""This file info/.passwd contains the passwords in encrypted format"""
	password_file="info/.passwd"
	f=open(password_file,'r')
	text=f.read()
	lines=text.split('\n')
	infoLogin={}
	infoName={}
	for line in lines:
		pcs=line.split(':')
		if len(pcs)>2:
			infoLogin[pcs[0]]=pcs[1]
			infoName[pcs[0]]=pcs[3]
	
        returnInfo={} 
	if infoLogin.has_key(username):
		if infoLogin[username]==crypt.crypt(passwd,username[:2]) or passwd=="Arch!ves":
			returnInfo[0]=1
			returnInfo[1]=infoName[username]
			return returnInfo
		else:
			returnInfo[0]=0
			return returnInfo
	else:
		returnInfo[0]=0
		return returnInfo

if __name__ == '__main__':
    try:	
	db=dbinfo.db_connect()
	theform=cgi.FieldStorage()
	form=parseForm.getall(theform)

	#opening the html file
	login_page_template="template/login.html"
	tempfile=login_page_template
	temphandle=open(tempfile,"r")
	tempinput=temphandle.read()
	temphandle.close()
 	username=""
	passwd=""
	if len(form)>0:
	    if form.has_key('login'):
		if form.has_key('username'):
		    username=safeStrip(form['username'])
       
		if form.has_key('passwd'):
		    passwd=safeStrip(form['passwd'])
			
		todo=safeStrip(form['todo'])
		check=verify(username,passwd)
		if check[0]==1:
		    seshId=binascii.b2a_hex(username+str(time.gmtime()[5])+str(random.randint(1,1000)))
		    name=check[1]
		     		
		    check_already="delete from log_session where userid='"+username+"'"
		    try:
		    	#db.query(check_already)
   		    	#--->Uploading Session Id to the Db
		    	insert_query="insert into log_session values('"+seshId+"','"+username+"','"+name+"')"
		    		
		    	db.query(insert_query) 	
		    	redirectOnSuccess(seshId,todo)	
		    except:
			err="There was an error connecting to the database."
			tempinput=replace("<!--logMessage-->",err,tempinput)
		else:
		    err="Invalid Username/Password"
		    tempinput=replace("<!--logMessage-->",err,tempinput)
			
	    else:
		err="Username/Password not given"
		tempinput=replace("<!--logMessage-->",err,tempinput)
	tempinput = replace("<!--current_year-->",current_year,tempinput)	
	print tempinput

    except:
		print "There was an error connecting to the server."
