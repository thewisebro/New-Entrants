#!/usr/bin/python
""" 
This file handles all ajax queries passed through javascript
and returns responses in xml/html text format
"""

import os,sys
current_app_path=os.getcwd()
sys.path.append(current_app_path+"/modules")

import cgi
import cgitb

import parseForm,dbinfo
from include import *

db=dbinfo.db_connect()
print "Content-Type:text/html\n"



def get_notices_list(notice,after,mx):
    """
    returns new/old notices information in xml format
    parmeter:
       notice = "new" or "old"
       after = <a number>
       mx = <a number> or "all"
    """
    notices = "notices"
    if notice == "old":
        notices = "old_notices"
    result = db.query("select * from " + notices + " order by to_timestamp(date,'DD-MM-YYYY HH:MI AM') desc;")
    rslt = result.dictresult()
    xml = ""
    length = len(rslt)
    after = int(after) 
    nomore = "false"
    if after >= length:
        return "<status>failure</status>\n<nomore>true</nomore>\n"
    else: 
        xml += "<status>success</status>\n"
    if mx == 'all' :
        mx = length-after
	nomore = "true"
    else: 
        mx = int(mx)
    if (after+mx) >= length:
        mx = length-after;
	nomore = "true"
    xml += "<nomore>" + nomore + "</nomore>\n"
    xml += "<total>" + str(length) + "</total>\n"
    for i in range(after,after+mx):
        row = rslt[i]
        ntc = "<notice>\n"
        ntc += "<id>" + str(row['id']) + "</id>\n"
        ntc += "<subject>" + ampEscape(row['subject']) + "</subject>\n"
        #ntc += "<date>" + row['date'].split(' ')[0] + "</date>\n"
        ntc += "<date>" + row['date'] + "</date>\n"
        ntc += "<reference>" + row['reference'] + "</reference>\n"
        ntc += "<from>" + row['sent_from'] + "</from>\n"
        ntc += "<to>" + row['sent_to'] + "</to>\n"
        ntc += "</notice>\n"
        xml += ntc
    return xml




def getNotice(ide):
    """
    This function returns notice content as html format
    parameter:
       ide = id of notice
    """
    html = ""
    result = db.query("select * from notices where id="+ide+";")
    if len(result.dictresult()) == 0:
        result = db.query("select * from old_notices where id="+ide+";")
        if len(result.dictresult()) == 0:
            return html + "failure</body></html>"
    notice = result.dictresult()[0]
    content = ""
    try:
        tempfile = "data/n" + ide
        temphandle = open(tempfile,"r")
        tempinput = temphandle.read()
        temphandle.close()
	#convert static url on people to relative
	tempinput = tempinput.replace("http://people.iitr.ernet.in/Notices","/notices")
        content += tempinput
    except Exception:
        return html + "failure"
    div = "<div id=\"content\" >\
           <div id=\"content-header\" >\
           <div id=\"content-subject\" ><b>Subject : </b> "+notice['subject']+"</div>\
           <div id=\"content-reference\"><b>Reference No. : </b>"+notice['reference']+"</div>\
	   <div style=\"clear:both\"></div></div>"

    content = "<div id=\"content-main\" >"+content+"</div></div>"
    html += div+content
    return html
 



def makeSearch(exprsn,adv):
    """
    Searches and returns the matched notices infos in xml format
    parameter:
       exprsn = expression to be searched
       adv = a list; may have elements: "new","old","subject","content","date"       
    """
    expr = ""
    for l in exprsn:
        if l.isalnum() or l == ' ' or l == '-':
            expr += l
        _words = expr.split(' ')
    
    words = []
    for word in _words:
        if not word == '':
            words.append(word)
    
    if len(words) == 0 :return "<status>failure</status>\n"
 
    if (not "new" in adv and not "old" in adv) or (not "subject" in adv and not "content" in adv and not "date" in adv):
        return "<status>failure</status>\n"
 
    idees = [] 
    xml = ""
    if "subject" in adv or "date" in adv:
    
        s = ""
        s += "subject ilike '%"+words[0]+"%'"
        for i in range(1,len(words)):
            s += " or subject ilike '%"+words[i]+"%'"
        d = ""
        d += "date ilike '%"+words[0]+"%'"
        for i in range(1,len(words)):
            d += " or date ilike '%"+words[i]+"%'"

        result = 0
        j = ""

        if "subject" in adv:
            j = s
	    if "date" in adv:
                j += " or "+d
        else:    
	    j = d  
 
        if "new" in adv and not "old" in adv:
            result = db.query("select id from notices where "+j+" order by id desc;")
    
        elif "old" in adv and not "new" in adv:
            result = db.query("select id from old_notices where "+j+" order by id desc;")

        else:
            result = db.query("select id from notices where "+j+" union\
                        select id from old_notices where "+j+" order by id desc;")
   
        rslt = result.dictresult()
        for row in rslt:
             idees.append(str(row['id']))

    if "content" in adv:
        for word in words:
            p = os.popen("grep -i -l '"+word+"' data/*")
            outs = p.read()
            p.close()
            outs = outs.split('\n')
            outs = outs[:-1]
            for idee in outs:
                if not idee[6:] in idees:
                    idees.append(idee[6:])
 
    ids=[]
    if "new" in adv:
        for idee in idees:
            if len(db.query("select id from notices where id="+idee+";").dictresult()) == 1:
	        ids.append(idee)
    if "old" in adv:
        for idee in idees:
            if len(db.query("select id from old_notices where id="+idee+";").dictresult()) == 1:
	        ids.append(idee)
 	    
    if len(ids) == 0:return "<status>failure</status>\n"
    xml += "<status>success</status>\n"
    xml += "<total>"+str(len(ids))+"</total>\n" 

    for idee in ids:
        result = db.query("select * from notices where id="+idee+" union select * from old_notices where id="+idee+";")
        rslt = result.dictresult()
        if(len(rslt) == 1):
            row = rslt[0]
            ntc = "<notice>\n"
            ntc += "<id>" + str(row['id']) + "</id>\n"
            ntc += "<subject>" + ampEscape(row['subject']) + "</subject>\n"
            ntc += "<date>" + row['date'].split(' ')[0]+"</date>\n"
            ntc += "<reference>" + row['reference'] + "</reference>\n"
            ntc += "<from>" + row['sent_from'] + "</from>\n"
            ntc += "<to>" + row['sent_to']+"</to>\n"
            ntc += "</notice>\n"
            xml += ntc
    return xml




  



if __name__=="__main__":
    """
    queries have keys:
        action  (values = 'new_notice' or 'old_notices' or 'getnotice' or 'search')
            >>in case of 'new_notices' or 'old_notices' extra keys are:
        after , 
	max
	    >>in case of 'getnotice' extra key is:
        id
	    >>in case of 'search' extra key are:
	expr,
	adv (for advance search; may have multiple values from 'new','old','subject','content','date')

    """
    theform = cgi.FieldStorage()
    form = parseForm.getall(theform)
    xml = "<?xml version='1.0' encoding='UTF-16'?>\n<root>\n"
    if form.has_key('action'):
        act = form['action']
        if (act == 'new_notices' or act == 'old_notices') and form.has_key('after')\
                and form.has_key('max') and form['after'].isdigit() and (form['max'] == 'all' or form['max'].isdigit()):
            n = 'new'
            if act == 'old_notices':n='old'
            xml += get_notices_list(n,form['after'],form['max'])
        elif act == 'getnotice' and form.has_key('id') and form['id'].isdigit():
            print getNotice(safeStrip(form['id']))
            exit()
        elif act == 'search' and form.has_key('expr') and form.has_key('adv'):
            xml += makeSearch(safeStrip(form['expr']),safeStrip(form['adv']))
        else:
            xml += "<status>failure</status>\n"
    else:
        xml += "<status>failure</status>\n"
    xml += "</root>"
    print xml
 
