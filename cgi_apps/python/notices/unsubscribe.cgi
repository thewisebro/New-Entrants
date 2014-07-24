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

def showPage(unsubscribed):
    if unsubscribed :
	print '''<html><head></head><body>Unsubscription Successful</body></html>'''
    else:
        print '''<html><head></head><body>Unsubscription Failure</body></html>'''


				
def confirmPage(key):
    print '''<html><head></head><body>Unsubscribe eNotices from Notice Board<br>
             <form action="unsubscribe.cgi" method="get">
	     <input type="hidden" name="key" value="'''+key+'''">
	     <input type="submit" name="confirm" value="Confirm"><form></body></html>'''


if __name__ == '__main__':

	theForm=cgi.FieldStorage()
	form=parseForm.getall(theForm)

	if len(form)>0:


		if form.has_key('key'):
		      key=form['key'] 
		      if form.has_key('confirm'):
				result=db.query("select * from student_preference where key='"+safeStrip(key)+"';")
				if len(result.dictresult()) == 1:
				    delete_query="delete from student_preference where key='"+safeStrip(key)+"';"
			            try:
				        db.query(delete_query) 	
				    except error:
				        showPage(False)
                                    else:
				        showPage(True)	
			        else:
				    showPage(False)
		      else:
		                confirmPage(key);
        	else:
			showPage(False)
	else:
		showPage(False)

