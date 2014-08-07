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
from include import *

print "Content-Type: text/html\r"
print "Cache-Control:private,no-cache,no-store,must-revalidate\r\n\r\n"

db=dbinfo.db_connect()

def redirect2Login():
    print '''<html><head>\
          <script type="text/javascript">\
	  document.location="index.cgi"\
	  </script></head></html>'''

				

if __name__ == '__main__':

    theForm=cgi.FieldStorage()
    form=parseForm.getall(theForm)

    if len(form)>0:
        
	if form.has_key('auth'):
            seshId=form['auth']
	    #--->Deleting Session Id from the Db
	    delete_query="delete from log_session where sid='"+seshId+"'"
            db.query(delete_query) 	
            redirect2Login()	
	else:
	    redirect2Login()
    else:
        redirect2Login()
				
