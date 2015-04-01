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
srch['str']  =functions.remove_special_characters(form.getvalue("Name", ""))
srch['categ']=form.getvalue("search_category","all")
srch['adv']   =form.getvalue("advanced_search_status","off")
stud['prog'] =form.getvalue("student_programme","null")
stud['year'] =form.getvalue("student_year","null")
stud['dept'] =form.getvalue("student_deptt","null")
fac['dept']  =form.getvalue("faculty_deptt","null")
fac['post']  =form.getvalue("faculty_post","null")
serv['name'] =form.getvalue("services_list","null")
searching    =form.getvalue("form_submitted","true")	#true if form was submitted else false
form_data    ={'srch':srch,'stud':stud,'fac':fac,'serv':serv}
if functions.is_all_null(form_data)=="true" and len(srch['str'])==0:
	searching="false"	
#read contents of htmlcode.htm
if searching == "false":
	html     = open("./htmlcode.htm","rb")
else :	
	html     = open("./results.html","rb")
contents = html.readlines()
html.close()
#get data for form dynamically from db
dept_list = db_queries.get_departments()
serv_list = db_queries.get_services()
post_list = db_queries.get_fac_posts()
disc_list = db_queries.get_disciplines()
#Prints the html contents and calls printr to print results if a query is submitted
for line in contents:
	line=line.strip()
	if not line.find('""')==-1:
		if not srch['str']=="":
			line=line.replace('""','"'+srch['str']+'"')
	print line
	if not line.find("<!--Search Results-->")==-1:
		try:
			if searching=="true":
				printr.printresult(form_data)
		except:
			print "Service unavailable this time.Please try ;ater after sometime."
	if not line.find("<!--Disciplines here-->")==-1:
		print '<option value="null">Select Discipline</option>'
		for discipline in disc_list:
			print '<option value="'+discipline['code']+'">'+discipline['corresponds_to']+'</option>'
	if not line.find("<!--Departments here-->")==-1:
		print '<option value="null">Select Department</option>'
		for dept in dept_list:
			print '<option value="'+dept['department_code']+'">'+dept['department_name']+'</option>'
	if not line.find("<!--Services list here-->")==-1 :
		print '<option value="null">Select Service</option>'
		for entry in serv_list:
			print '<option value="'+entry['type']+'">'+entry['type']+'</option>'
	if not line.find("<!--Posts here-->")==-1:
		print '<option value="null">Select Designation</option>'
		for post in post_list:
			print '<option value="'+str(post['post'])+'">'+post['post_name']+'</option>'
