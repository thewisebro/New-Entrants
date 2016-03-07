#!/usr/bin/python
import printr
import cgi
import db_queries
import cgitb; cgitb.enable()  # for troubleshooting
import functions

print "Content-Type: text/html\n\n"

#form data if submitted
srch={}
stud={}
fac ={}
serv={}
form         = cgi.FieldStorage()
srch['str']  =form.getvalue("Name","")
srch['categ']=form.getvalue("search_category","null")
srch['adv']  =form.getvalue("advanced_search_status","null")
stud['prog'] =form.getvalue("student_programme","null")
stud['year'] =form.getvalue("student_year","null")
stud['dept'] =form.getvalue("student_deptt","null")
fac['dept']  =form.getvalue("faculty_deptt","null")
fac['post']  =form.getvalue("faculty_post","null")
serv['name'] =form.getvalue("services_list","null")
searching    =form.getvalue("form_submitted","false")	#true if form was submitted else false
#if form.getvalue("advanced_search_status")=="off":
#	srch['categ']="all"
form_data    ={'srch':srch,'stud':stud,'fac':fac,'serv':serv}
if (functions.is_all_null(form_data)=="true" or srch['adv']=="off") and len(srch['str'])==0:
	searching="false"
#remove special characters to avoid SQL injection
form_data['srch']['str']=functions.remove_special_characters(form_data['srch']['str'])
	
	
try:	
	#Prints the html contents and calls printr to print results if a query is submitted
	if searching == "true":
		printr.printresult(form_data)
except:
	print "<p>Service unavailable at this time.Please try after sometime.</p>"
