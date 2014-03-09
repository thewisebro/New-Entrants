#!/usr/bin/python
import sys
import os

current_app_path=os.getcwd()
#--->citing the path where user defined modules are stored
sys.path.append(current_app_path+"/modules")

import cgi
import cgitb
import parseForm
import dbinfo
from datetime import datetime
import random
from include import *

print "Content-Type: text/html\n\n"
db=dbinfo.db_connect()

def checkDb():
    """This function checks for notices that have been expired and 
    transfers expired notices from table notices to old_notices"""    
    today = datetime.today().strftime("%Y-%m-%d")
    result = db.query("select date from last_checked;").dictresult()
    if result[0]["date"]==today:return
    db.query("update last_checked set date='"+today+"';")
    result=db.query("select id,expire_date from notices;") 
    rslt=result.dictresult()
    for row in rslt:
        id=row['id']
        exp_date=row['expire_date']
        dmy=exp_date.split('-')
        exp_stmp=int(dmy[2]+dmy[1]+dmy[0])
        stmp=int(datetime.today().strftime("%Y%m%d"))
        if stmp>exp_stmp:
            db.query("insert into old_notices select * from notices where id="+str(id)+";")
            db.query("delete from notices where id="+str(id)+";")

  


script=""
if __name__=='__main__':
    checkDb()
    theform = cgi.FieldStorage()
    form = parseForm.getall(theform)
    sid = ""
    if form.has_key("sessionid"):
        sid = form['sessionid']
    open_notice_id = ""
    if form.has_key('id'):
        open_notice_id = form['id']
    tempfile="template/index.html"    
    temphandle=open(tempfile,"r")
    tempinput=temphandle.read()
    temphandle.close()

    cats=""
    for cat in Categories:cats+="'"+cat+"',"
    cats=cats[:-1]
    script+="var Categories=Array("+cats+");\n"
    for cat in Categories:
        Cat=eval(cat)
        CatOrder=eval(cat+"_order")
        subcats=""
        for subcat in CatOrder:
            subcats+="'"+subcat+":"+Cat[subcat]+"',"
        subcats=subcats[:-1]
        script+="var "+cat+"=Array("+subcats+");\n"
  
    tempinput = replace("<!--script-->",script,tempinput)
    tempinput = replace("<!--sid-->",sid,tempinput)
    tempinput = replace("<!--open_notice_id-->",open_notice_id,tempinput) 
    tempinput = replace("<!--current_year-->",current_year,tempinput)
    print tempinput
