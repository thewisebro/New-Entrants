#!/usr/bin/python

"""This script handles all Uploading,saving,re_editing,deleting functionalities
"""


import sys
import os
current_app_path = os.getcwd()
#--->citing the path where user defined modules are stored
sys.path.append(current_app_path + "/modules")

import cgi
import cgitb
import parseForm
import dbinfo
import subprocess
from datetime import datetime
from constant import *
from include import *


print "Content-Type: text/html\r"
print "Cache-Control:private,no-cache,no-store,must-revalidate\r\n\r\n"
db=dbinfo.db_connect()
    


def redirect2Login():
    print '''<html><head>\
	     <script type="text/javascript">\
	     document.location="login.cgi"\
	     </script></head></html>'''

def redirect2Editpage(seshid):
    print '''<html><head>\
            <script type="text/javascript">document.location="upload.cgi?auth='''+seshid+'''&todo=edit"</script>\
	    </head></html>'''


def link2Upload(seshid,message):
    print "<html><body>"+message+"<br>\
            <a href=\"upload.cgi?auth="+seshid+"&todo=upload\">Back to upload page</a>\
	    </body></html>"


def link2Editpage(seshid,message,idee):
    print "<html><body>"+message+"<br>\
           <a href=\"upload.cgi?auth="+seshid+"&todo=edit&id="+idee+"\">Back to Edit page</a>\
	   </body></html>"

def link2Editlinkspage(seshid,message):
    print "<html><body>"+message+"<br>\
           <a href=\"upload.cgi?auth="+seshid+"&todo=edit\">Back to Edit page</a>\
	   </body></html>"




def isLoggedIn(seshid):
    """returns True/False according to authority is loggedIn or not
    """
    result = db.query("select * from log_session where sid='"+seshid+"'")
    if len(result.dictresult()) == 0:return False
    else: return True


def CategoryTable():
    """Returns html for category sub-category table
    """
    table = ""
    for cat in Categories:
        Cat = eval(cat)
        Cat_order = eval(cat + "_order")
        div = "<div class=\"category\">\n<b>" + cat + "</b>\n"     
        if len(Cat_order) > 1:
            div += "<div class=\"subcat\">\n"
	    div += "<input type='checkbox' id='"+cat+"'onclick=\"clickall('"+cat+"')\">"+\
	           "<label for='"+cat+"'>All</label>"
	    div += "</div>\n"
        for subcat in Cat_order:
	    div += "<div class=\"subcat\">\n"
            div += "<input type='checkbox' name='"+cat+"'"+\
	           "value='"+subcat+"' id='"+subcat+"'>\n"+\
	           "<label for='"+subcat+"'>"+Cat[subcat]+"</label>\n"
	    div += "</div>\n"
        div += "</div>\n"
        table += div
    return table   



def uploadnotice(seshid,premsg=""):
    """Prints Upload Page
    """
    userid = db.query("select * from log_session where sid='"+seshid+"';").dictresult()[0]['userid']
    upload_page_template = "template/upload.html"
    tempfile = upload_page_template
    temphandle = open(tempfile,"r")
    tempinput = temphandle.read()
    temphandle.close()
 
    script = ""
    cats = ""
    for cat in Categories:cats += "'"+cat+"',"
    cats = cats[:-1]
    script += "var Categories=Array("+cats+");\n"
  
    tempinput = replace("<!--script-->",script,tempinput)

    tempinput = replace("<!--todo-->","save",tempinput)
    tempinput = replace("<!--userid-->",userid,tempinput)
    tempinput = replace("<!--sid-->",seshid,tempinput)
    tempinput = replace("<!--ctable-->",CategoryTable(),tempinput)
    tempinput = replace("<!--premsg-->",premsg,tempinput)
    tempinput = replace("<!--current_year-->",current_year,tempinput)
    
    for i in range(5):
      tempinput = replace("<!--curr_year" + str(i) + "-->",str(curr_year+i),tempinput)
         
    print tempinput




def save2db(seshid,subject,ckbody,ref,date_exp,month_exp,year_exp,ctgrs,idee=None,date_created=None):
    """Saves a notice(all information) into db
       If extra parameter(idee,date_created) also passed then it assumes that 
       notice has been re_edited then
       it makes changes in the notice that is already in db
    """
    expire_date = datetime(year_exp,month_exp,date_exp).strftime("%d-%m-%Y")
    current_time = datetime.today().strftime("%d-%m-%Y %I:%M %p")
    nextid=0
    if not idee:
        nextid = str(  db.query("select nextval('notice_id_sequence') as id;").dictresult()[0]['id']  )
    else :
        nextid = idee    
    db.query("insert into notices(id) values("+nextid+");")
    if idee:
        db.query("update notices set date_created='"+date_created+"' where id="+nextid+";")
    else:
        db.query("update notices set date_created='"+current_time+"' where id="+nextid+";")

    db.query("update notices set subject='"+subject+"' where id="+nextid+";")
    db.query("update notices set date ='"+current_time+"' where id="+nextid+";")
    db.query("update notices set expire_date ='"+expire_date+"' where id="+nextid+";")
    db.query("update notices set reference ='"+ref+"' where id="+nextid+";" )
    q = "select * from log_session where sid='"+seshid+"';"
    result = db.query(q)
    userid = result.dictresult()[0]['userid']
    name = result.dictresult()[0]['name']
    db.query("update notices set sent_from ='"+name+"' where id="+nextid+";")
    db.query("update notices set user_id ='"+userid+"' where id="+nextid+";")
    sent_to = ""
    for cat in ctgrs.keys():
        sent_to += cat+":"+ctgrs[cat]+"|"
    sent_to = sent_to[:-1] 
    db.query("update notices set sent_to ='"+sent_to+"' where id="+nextid+";") 
    if idee:
        db.query("update notices set re_edited ='yes' where id="+nextid+";")
        os.popen("mv --backup=t "+current_app_path+"/data/n"+nextid+" "+current_app_path+"/data/archives/n"+nextid+"_bk")
    file = open(current_app_path+"/data/n"+nextid,"wr+")
    file.write(ckbody)
    file.close()





def isComplete(form):
    """Checks if all data in form-keys is given or not
    It returns a result dict.
    If form is complete then sets key 'value' = True
    Else sets key 'value' = False
    And fills all other key-value pairs of form in result dict
    """
    result = {}
    result['value'] = False
    m = ""
    flag = True
    if not form.has_key('subject'):m += "Subject field is empty;";flag = False
    if not form.has_key('date_exp'):m += "Expire Date not given;";flag = False
    if not form.has_key('month_exp'):m += "Expire Month not given;";flag = False
    if not form.has_key('year_exp'):m += "Expire Year not given;";flag = False
    if not form.has_key('ckbody'):m += "No content in Notice;";flag=False
    if flag == False:result['message'] = m;return result
    flag = False;
    for i in range(len(Categories)):
        if form.has_key(Categories[i]):
            flag = True
    if flag == False:
        result['message'] = "No category is checked;"
        return result;
    subject = safeStrip(form['subject'])
    date_exp = safeStrip(form['date_exp'])
    month_exp = safeStrip(form['month_exp'])
    year_exp = safeStrip(form['year_exp'])
    if form.has_key('ref'):ref = safeStrip(form['ref']) 
    else : ref="null"  
    ckbody = form['ckbody']
    flag = True;m = ""
    if subject == "" : m += "Subject field is empty;";flag = False
    if date_exp == "-1" or not date_exp.isdigit() : m += "Expire Date not defined;";flag = False
    if month_exp == "-1" or not month_exp.isdigit(): m += "Expire Month not defined;";flag = False
    if year_exp == "-1" or not year_exp.isdigit(): m +=  "Expire Year not defined;";flag = False
    if ref == "": ref=="null"
    if ckbody == "": m += "Notice Content is empty;";flag = False
    if flag == False :result['message'] = m;return result
    try:
        datetime(int(year_exp),int(month_exp),int(date_exp))
    except:
        result['message'] = "Expire date given is not correct;";return result
    if int(datetime.today().strftime("%Y%m%d")) > int(datetime(int(year_exp),int(month_exp),int(date_exp)).strftime("%Y%m%d")):
        result['message'] = "Expire date given is a past date;";return result
    result['value'] = True
    result['subject'] = subject
    result['date_exp'] = int(date_exp)
    result['month_exp'] = int(month_exp)
    result['year_exp'] = int(year_exp)
    result['ref'] = ref
    result['ckbody'] = correct_urls(ckbody)
    return result
 



def savenotice(seshid,form):
    """Saves a uploaded notice
    """
    result = isComplete(form)
    if result['value'] == False:
        uploadnotice(seshid,result['message'])
        return  
  
    ctgrs = {}
    for i in range(len(Categories)):
        subcats = ""
        if form.has_key(Categories[i]):
            if not type(form[Categories[i]]) == type([]):subcats+=form[Categories[i]]
            else:
                for subcat in form[Categories[i]]:
                    subcats += str(subcat)+','
                subcats = subcats[:-1]
            ctgrs[Categories[i]] = subcats
  
    save2db(seshid,result['subject'],result['ckbody'],result['ref'],result['date_exp'],result['month_exp'],result['year_exp'],ctgrs);
    showeditnotices(seshid,"Upload Successfull")



def showeditnotices(seshid,premsg=""):
    """Prints the htmlpage to show list of all edited notices of authority user
    """
    result = db.query("select * from log_session where sid='"+seshid+"';").dictresult()[0]
    userid = result['userid']
    user_notices = db.query("select * from notices where user_id='"+userid+"' order by id desc;").dictresult()
    user_old_notices = db.query("select * from old_notices where user_id='"+userid+"' order by id desc;").dictresult()
    links_new = ""
    links_old = ""
    for notice in user_notices:
        links_new += "<div class=\"noticeinfo\" >\
                <a style=\"float:left;text-decoration:none\" href=\"upload.cgi?auth="\
		+seshid+"&todo=edit&id="+str(notice['id'])+"\">"+notice['subject']+"</a>\
                <a style=\"float:right\" href=\"upload.cgi?auth="+\
		 seshid+"&todo=delete&id="+str(notice['id'])+"\" onclick=\"return \
		 confirm('Do you really want to parmanently delete this notice?');\">Delete</a></div>\n"
    for notice in user_old_notices:
        links_old += "<div class=\"noticeinfo\">\
                <a style=\"float:left;text-decoration:none\" href=\"upload.cgi?auth="\
		+seshid+"&todo=edit&id="+str(notice['id'])+"\">"+notice['subject']+"</a>\
                <a style=\"float:right\" href=\"upload.cgi?auth="+\
		 seshid+"&todo=delete&id="+str(notice['id'])+"\" onclick=\"return \
		 confirm('Do you really want to parmanently delete this notice?');\">Delete</a></div>\n"

 
    tempfile = "template/editlinks.html" 
    temphandle = open(tempfile,"r")
    tempinput = temphandle.read()
    tempinput = replace("<!--sid-->",seshid,tempinput)
    tempinput = replace("<!--userid-->",userid,tempinput)
    tempinput = replace("<!--list_of_notices-->",links_new,tempinput)
    tempinput = replace("<!--list_of_old_notices-->",links_old,tempinput)
    tempinput = replace("<!--premsg-->",premsg,tempinput)
    temphandle.close()
    tempinput = replace("<!--current_year-->",current_year,tempinput)
    print tempinput




def edit(seshid,noticeid,premsg=""):
    """Prints htmlpage for re_editing a notice
    """
    result = db.query("select * from log_session where sid='"+seshid+"';").dictresult()[0]
    userid = result['userid']
    typeofnotice = "new"
    result = db.query("select * from notices where user_id='"+userid+"' and id="+noticeid+";").dictresult()
    notice = 0
    if len(result) == 1:
        notice = result[0]
    else: 
        result = db.query("select * from old_notices where user_id='"+userid+"' and id="+noticeid+";").dictresult()
        if len(result) == 1:
            notice = result[0]
            typeofnotice = "old"
        else:
            redirect2Editpage(seshid)
    subject = notice['subject']
    dmy = notice['expire_date'].split('-')
    expdate = dmy[0]
    expmonth = dmy[1]
    expyear = dmy[2]
    if expdate[0] == '0':expdate=expdate[1:]
    if expmonth[0] == '0':expmonth=expmonth[1:]
    refno = notice['reference']
    if refno == 'null':refno = ''
  
    datafile = open("data/n"+noticeid,"r")
    content = remove_pdfimages(datafile.read())
    datafile.close()
   
    script = "var Categories=Array("
    catsubcats = notice['sent_to'].split('|')
    
    for catsubcat in catsubcats:
        script += "'"+catsubcat.split(':')[0]+"',"
    script = script[:-1] + ");\n"
    
    for catsubcat in catsubcats:
        cat = catsubcat.split(':')[0]
        subcats = catsubcat.split(':')[1].split(',')
        script += "var checked_"+cat + "=Array("
        for subcat in subcats:
            script += "'"+subcat+"',"
        script = script[:-1]+");\n"
  
    edit_page_template = "template/edit.html"
    tempfile = edit_page_template
    temphandle = open(tempfile,"r")
    tempinput = temphandle.read()
    temphandle.close()
    tempinput = replace("<!--id-->",noticeid,tempinput)
    tempinput = replace("<!--todo-->","savechanges",tempinput)
    tempinput = replace("<!--subject-->",subject,tempinput)
    tempinput = replace("<!--date-->",expdate,tempinput)
    tempinput = replace("<!--month-->",expmonth,tempinput)
    tempinput = replace("<!--year-->",expyear,tempinput)
    tempinput = replace("<!--refno-->",refno,tempinput)
    tempinput = replace("<!--script-->",script,tempinput)
    tempinput = replace("<!--sid-->",seshid,tempinput)
    tempinput = replace("<!--content-->",content,tempinput) 
    tempinput = replace("<!--userid-->",userid,tempinput)
    tempinput = replace("<!--premsg-->",premsg,tempinput)
    tempinput = replace("<!--ctable-->",CategoryTable(),tempinput)
    tempinput = replace("<!--current_year-->",current_year,tempinput)
    for i in range(5):
      tempinput = replace("<!--curr_year" + str(i) + "-->",str(curr_year+i),tempinput)   
    print tempinput

 



def savechanges(seshid,form):
    """saves and makes changes in db after re_editing of a notice
    """
    noticeid = safeStrip(form['id'])
    result = db.query("select * from log_session where sid='"+seshid+"';").dictresult()[0]
    userid = result['userid']
    typeofnotice = "new"
    result = db.query("select * from notices where user_id='"+userid+"' and id="+noticeid+";").dictresult()
    notice = 0
    if len(result) == 1:
        notice = result[0]
    else: 
        result = db.query("select * from old_notices where user_id='"+userid+"' and id="+noticeid+";").dictresult()
        if len(result) == 1:
            notice = result[0]
            typeofnotice = "old"
        else:
            redirect2Editpage(seshid)
  
    result = isComplete(form)
    if result['value'] == False:
        edit(seshid,noticeid,result['message'])
        return 
    if typeofnotice == "new":
        db.query("insert into trash_notices select * from notices where id="+noticeid+";")
        db.query("delete from notices where id="+noticeid+";")

    
    ctgrs={}
    for i in range(len(Categories)):
        subcats = ""
        if form.has_key(Categories[i]):
            if not type(form[Categories[i]]) == type([]):subcats+=form[Categories[i]]
            else:
                for subcat in form[Categories[i]]:
                    subcats += str(subcat)+','
                subcats = subcats[:-1]
            ctgrs[Categories[i]] = subcats
    
    if typeofnotice == "new" :  
        save2db(seshid,result['subject'],result['ckbody'],result['ref'],result['date_exp'],
	        result['month_exp'],result['year_exp'],ctgrs,noticeid,notice['date_created'])
    else :
        save2db(seshid,result['subject'],result['ckbody'],result['ref'],result['date_exp'],result['month_exp'],result['year_exp'],ctgrs)     
    showeditnotices(seshid,"Changes Successfull")




def delete(seshid,noticeid):
    """deletes a notice from notices,old_notices and inserts that into trash_notices
    """
    noticeid = safeStrip(form['id'])
    result = db.query("select * from log_session where sid='"+seshid+"';").dictresult()[0]
    userid = result['userid']
    typeofnotice = "new"
    result = db.query("select * from notices where user_id='"+userid+"' and id="+noticeid+";").dictresult()
    notice = 0
    if len(result) == 1:
        notice = result[0]
    else: 
        result = db.query("select * from old_notices where user_id='"+userid+"' and id="+noticeid+";").dictresult()
        if len(result) == 1:
            notice = result[0]
            typeofnotice = "old"
        else:
            redirect2Editpage(seshid)
  
    if typeofnotice == "new":
        db.query("insert into trash_notices select * from notices where id="+noticeid+";")
        db.query("delete from notices where id="+noticeid+";")
    else:
        db.query("insert into trash_notices select * from old_notices where id="+noticeid+";")
        db.query("delete from old_notices where id="+noticeid+";")
  
    os.popen("mv --backup=t "+current_app_path+"/data/n"+noticeid+" "+current_app_path+"/data/archives/n"+noticeid+"_bk")
  
    showeditnotices(seshid,"Delete Successfull")



if __name__=='__main__':
    """This handles all queries and passes controls to functions
    according to queries.
    """
    theform = cgi.FieldStorage()
    form = parseForm.getall(theform)
    
    if len(form)<2:redirect2Login()
    elif not form.has_key('auth') or not form.has_key('todo'):redirect2Login()
    else:
        seshid = safeStrip(form['auth'])
        todo = safeStrip(form['todo'])
        if not isLoggedIn(seshid):redirect2Login()
        else:
            if todo == 'upload':uploadnotice(seshid)
            elif todo == 'edit':
	        if form.has_key('id'):edit(seshid,safeStrip(form['id']))
	        else:showeditnotices(seshid)
	    elif todo == 'delete':
	        if form.has_key('id'):delete(seshid,safeStrip(form['id']))
	        else:showeditnotices(seshid)
	    elif todo == 'save':
	        savenotice(seshid,form)
          # Sendmail script run by cronjob
          #subprocess.Popen("./sendmail.py")
	    elif todo == 'savechanges':
	        savechanges(seshid,form)
          # Sendmail script run by cronjob
          #subprocess.Popen("./sendmail.py")
	    else: 
	        redirect2Login()

