#!/usr/bin/python
import sys
import os
current_app_path = os.getcwd()
#--->citing the path where user defined modules are stored
sys.path.append(current_app_path+"/modules")

import cgi
import cgitb
import parseForm
import dbinfo
import binascii
import time
from datetime import datetime
import random
from include import *

print "Content-Type: text/html\n\n"
db = dbinfo.db_connect()

def channelI_link():
    """
    """
    return """Login to channel I to subscribe for E-Notices<br>
           <a href="http://192.168.121.7">Channel I</a>
	   """

def CategoryTable():
    """Creates Category-Subcategory table in html 
    """
    table=""
    for cat in Categories:
        Cat=eval(cat)
        Cat_order=eval(cat+"_order")
        div="<div class=\"category\">\n<b>"+cat+"</b>\n"     
        if len(Cat_order) >1:
            div+="<div class=\"subcat\">\n"
	    div+="<input type='checkbox' id='"+cat+"'onclick=\"clickall('"+cat+"')\">"+\
	         "<label for='"+cat+"'>All</label>"
	    div+="</div>\n"
        for subcat in Cat_order:
	    div+="<div class=\"subcat\">\n"
            div+="<input type='checkbox' name='"+cat+"'"+\
	         "value='"+subcat+"' id='"+subcat+"'>\n"+\
	         "<label for='"+subcat+"'>"+Cat[subcat]+"</label>\n"
	    div+="</div>\n"
        div+="</div>\n"
        table+=div
    return table   


def isvalidEmail(email):
    """
    """
    splits = email.split('@')
    if len(splits) == 2:
	if '.' in splits[1] :
	    return True
    return False	    

def check_session(sessionid):
    """
    """
    intranetdb = dbinfo.intranet_db_connect()
    result = intranetdb.query("SELECT username FROM session_id WHERE sessionid='"+sessionid+"';").dictresult()
    if len(result) > 0:
        return result[0]["username"]
    else:
        return None


def toDb(form,username):
    """
    Inserts a user email id and prefernces to db
    """
    if not form.has_key("email"):return False 
    email = safeStrip(form["email"])
    if not isvalidEmail(email):
        return "Invalid Email id"
    ctgrs = {}
    for i in range(len(Categories)):
        subcats = ""
        if form.has_key(Categories[i]):
            if type(form[Categories[i]]) != type([]):subcats += form[Categories[i]]
            else:
                for subcat in form[Categories[i]]:
                    subcats += str(subcat)+','
                subcats = subcats[:-1]
            ctgrs[Categories[i]] = subcats
    sent_to = ""
    for cat in ctgrs.keys():
        sent_to += cat+":"+ctgrs[cat]+"|"
    sent_to = safeStrip(sent_to[:-1])
    key=binascii.b2a_hex(username+str(time.gmtime()[5])+str(random.randint(1,1000)))
    db.query("delete from student_preference where userid = '"+username+"';") 
    db.query("INSERT into student_preference(userid,email_id,sent_to,key) values('"+username+"','"+email+"','"+sent_to+"','"+key+"');")
    return "You are subscribed"

def correct_db():
    result = db.query("select * from student_preference;").dictresult()
    for row in result:
        if len(key.split('.'))==2:
	    print row['user_id'],row['key']


if __name__ == '__main__':
    theform = cgi.FieldStorage();
    form = parseForm.getall(theform)
    username = None
    if form.has_key("sessionid"):
        sessionid = safeStrip(form["sessionid"])
	username = check_session(sessionid)
	if username == None:
	    print channelI_link()
            exit(0)	    
    else:	    
        print channelI_link()
	exit(0)
    msg=""
    email=""
    if form.has_key("subscribe"):
        msg = toDb(form,username)
    else :
        result = db.query("select * from student_preference where userid = '"+username+"';").dictresult()
	if len(result)==1:
	    email = result[0]['email_id']

    tempfile = "template/subscribe.html"
    temphandle = open(tempfile,"r")
    tempinput = temphandle.read()
    temphandle.close()
    script=""
    cats=""
    for cat in Categories:
        cats+="'"+cat+"',"
    cats=cats[:-1]
    script+="var Categories=Array("+cats+");\n"
    tempinput=replace("<!--script-->",script,tempinput)
    tempinput=replace("<!--sessionid-->",sessionid,tempinput)
    tempinput = replace("<!--table-->",CategoryTable(),tempinput)
    tempinput = replace("<!--premsg-->",msg,tempinput)
    tempinput = replace("<!--email-->",email,tempinput)
    tempinput = replace("<!--current_year-->",current_year,tempinput)
    print tempinput
  
