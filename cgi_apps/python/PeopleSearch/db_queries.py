#! /usr/bin/python
import db_connect
import db_queries
import functions
import soundx

db        =db_connect.connect_to_test()
regoldb   =db_connect.connect_to_regolj()
facappdb  =db_connect.connect_to_facapp()
cmsdb	  =db_connect.connect_to_cms()

#Table names
student_table ='person_soundx'
faculty_table ='person_list'
services_table='localnos'
#the next string is appended to each query for student and will exclude results with invalid course
valid_stud_courses=" and (p.course in (110,111,120,121,130,131,140,141,150,151) or (p.course>220 and p.course<229) or (p.course>320 and p.course<341))"


def student_name_query(name):
	"""Function to query by name in student table.Arguement required is name only"""
	splittedname=name.split(" ")
	result=[]
	query="select p.name,p.person_id,p.enrollment_no,c.corresponds_to as deptt,p.course,p.degree from person_extended p,codes_used c,person_soundx s where (%s or p.person_id ilike '%%"+name+"%%')"+valid_stud_courses+" and p.person_id=s.person_id and p.discipline=c.code "
	i=0
	condition=""
	for part in splittedname:
		if i==1:
			condition=condition+"and "
		i=1
		soundpart=soundx.soundxfunction(part)
		condition=condition+"s.soundx ilike '%"+soundpart+"%' "
	query=query%condition
	try:
		result=regoldb.query(query).dictresult()
	except Exception,e:
		print(e)
		exit()
	result=functions.sort_query(result,name)
#	print query
	return result




def faculty_name_query(name):
	"""Function to query by name in faculty table.Requires name as arguement"""
	splitname=name.split(" ")
	result=[]
	query="select f.name,f.faculty_id,f.department_code,m.post_name from post_mapping m,general_information f,fac_soundx s where m.post=f.post and f.faculty_id=s.faculty_id and %s"
	
	
	
	i=0
	condition=""
	for part in splitname:
		if i==1:
			condition=condition+"and "
		i=1
		soundpart=soundx.soundxfunction(part)
		condition=condition+"s.soundx ilike '%"+soundpart+"%' "
	query=query%condition
#	print query
	result=facappdb.query(query).dictresult()
	result=functions.sort_query(result,name,'faculty_id')
	result=assign_deptts(result)	#assign department names on the basis of department_code
	return result


def services_name_query(name):
	"""Function to query by name in services table.Requires name as arguement"""
	splitted_names=functions.split_the_name(name)
	result=[]
	query="select * from "+services_table+" where name is not null"
	for part in splitted_names:
		query=query+" and name ilike '%"+part+"%'"
	return db.query(query).dictresult()


def contact_num_query(contact_num):
	"""Search  by contact number in all the db.Requires contact number as arguement"""
	result=[]
	new_query=db.query("select * from "+student_table+" where contact_num ilike '%"+contact_num+"%'")
	result.extend(new_query.dictresult())
	new_query=db.query("select * from "+faculty_table+" where contact_num ilike '%"+contact_num+"%'")
	result.extend(new_query.dictresult())
	new_query=db.query("select * from "+services_table+" where contact_num ilike '%"+contact_num+"%'")
	result.extend(new_query.dictresult())
	result=functions.sort_query(result,contact_num)
	return result


def person_id_query(telnet_id):
	"""Search by telnet id in all the db.Requires telnet id as arguement."""
	result=[]
	telnet_id=telnet_id.lower().split('@')[0]
	new_query=db.query("select * from "+student_table+" where person_id ilike '%"+telnet_id+"%'")
	result.extend(new_query.dictresult())
	new_query=db.query("select * from "+faculty_table+" where person_id ilike '%"+telnet_id+"%'")
	result.extend(new_query.dictresult())
	result=functions.sort_query(result,telnet_id)
	return result





def get_departments():
	"""returns the dictionary of distinct departments for faculty"""
	return facappdb.query("select * from departments order by department_name").dictresult()


def get_disciplines():
	"""returns the dictionary of disciplines in person_extended table"""
	return regoldb.query("select * from codes_used where code in (select distinct(discipline) from person_extended) order by corresponds_to").dictresult()



def get_services():
	"""returns dictionary of different services from localnos table of test db"""
	services=db.query("select distinct(trim(type)) as type from localnos where type not in ('SCHOOLS AND COLLEGES','SELECTED LOCAL NOS.')")
	services=services.dictresult()
	return services

def get_fac_posts():
	"""Returns dictionary of different faculty posts from post_mapping table of facappn db."""
	posts=facappdb.query("select * from post_mapping order by post_name");
	posts=posts.dictresult()
	return posts




def run_query_on_test(query):
	"""runs the passed query on the test db.It returns the list of dictionary results"""
	res=db.query(query)
	res=res.dictresult()
	return res



def run_query_on_regolj(query):
	"""Runs the passed query on regolj db.It returns the pgqueryobject results"""
	res=regoldb.query(query)
	return res



def assign_deptts(list):
	"""Adds the column of deptt in the list of dictionaries passed as argument on the basis of the department_code"""
	depname=get_departments()
	depname=functions.to_dept_dict(depname)
	i=len(list)-1
	while i>=0:
		try:
			list[i]['deptt']=depname[list[i]['department_code']]
		except:
			#print "unknown deptt:"+list[i]['department_code']
			del list[i]		#delete the rows in which department code does not match a code in codes_used
		i=i-1
	return list

def exact_id_query(id):
	"""searches for the exact id in person_extended and faculty"""
	result={}
	query=regoldb.query("select p.enrollment_no,p.name,p.person_id,c.corresponds_to as deptt,p.course,p.degree from person_extended p,codes_used c where p.person_id = '"+id+"'"+valid_stud_courses+" and p.discipline=c.code")
	query=query.dictresult()
	result['stud']=query
	new_query=facappdb.query("select g.name,g.faculty_id,p.post_name,d.department_name as deptt from general_information g,post_mapping p,departments d where g.post=p.post and g.department_code=d.department_code and g.faculty_id = '"+id+"'")
	new_query=new_query.dictresult()
	result['fac']=new_query
	result['serv']={}
	return result



def adv_faculty(srch_str,fac_data):
	"""Handles the advanced faculty query if a selection is made on the drop down menu of faculty tab.Returns the dictionary containing the query result."""
	query="select g.name,g.faculty_id,g.department_code,m.post_name from general_information g,post_mapping m,fac_soundx f where (not(g.post=-1)) and g.faculty_id=f.faculty_id and g.post=m.post and (not(g.post=-1))"
	if fac_data['dept']!="null":
		query=query+" and g.department_code='"+fac_data['dept']+"'"
	if fac_data['post']!="null":
		query=query+" and g.post="+str(fac_data['post'])
	if srch_str!="":
		splitname=srch_str.split(" ")
		result=[]
		for part in splitname:
			soundpart=soundx.soundxfunction(part)
			query=query+" and f.soundx ilike '%"+soundpart+"%'"
	result=facappdb.query(query).dictresult()
	result=functions.sort_query(result,srch_str,'faculty_id')
	result=assign_deptts(result)	#assign department names on the basis of department_code
	return result



def adv_student(name,stud_data):
	"""Handles the advanced student search query.Input is dictionary of student data and output is query dictionary"""
	query="select p.name,c.corresponds_to as deptt,p.enrollment_no,p.person_id,p.course,p.degree from person_extended p,codes_used c,person_soundx s where p.person_id=s.person_id and p.discipline=c.code"
	condition="null"		#year and course condition
	if stud_data['dept']!="null":
		query=query+" and (p.discipline='"+stud_data['dept']+"')"
	if stud_data['prog']=="null" and stud_data['year']!="null":
		year=int(stud_data['year'])
		condition=" and (p.course in ("+str(100+year*10)+","+str(101+year*10)+","+str(219+year*2)+","+str(220+year*2)+","+str(319+year*2)+","+str(320+year*2)+"))"
	elif stud_data['year']=="null" and stud_data['prog']!="null":
		prog=int(stud_data['prog'])
		condition=" and (p.course<"+str(prog*100+100)+" and p.course>="+str(prog*100)+")"
	elif stud_data['year']!="null" and stud_data['prog']!="null":
		year=int(stud_data['year'])
		prog=int(stud_data['prog'])
		if stud_data['prog']=="1":
			condition=" and (p.course in (1"+stud_data['year']+"0,1"+stud_data['year']+"1))"
		else:
			condition=" and (p.course in ("+str(prog)+str(19+year*2)+","+str(prog)+str(20+year*2)+"))"
	else:
		condition=valid_stud_courses
	if condition!="null":
		query=query+condition
	if name!="":
		splitname=name.split(" ")
		if len(splitname)==1:
			query+=" and (p.person_id ilike '%"+name+"%' or s.soundx ilike '%"+soundx.soundxfunction(name)+"%')"
		else:
			for part in splitname:
				query=query+" and s.soundx ilike '%"+soundx.soundxfunction(part)+"%'"
	else:
		query+=" order by discipline,name"
#	print query
	result=regoldb.query(query).dictresult()
	if name != "":
		result=functions.sort_query(result,name)
	return result






def adv_services(srch_str,serv_data):
	"""Handles the advanced services query if a selelction is made on the drop down menu of services tab"""
	if srch_str=="":
		return db_queries.run_query_on_test("select * from localnos where type ='"+serv_data['name']+"'")
	que="select * from localnos where type='"+serv_data['name']+"' and name ilike '%"+srch_str+"%'"
	return db.query(que).dictresult()

def get_fac_url(fac_id):
	"""Returns the url of the faculty whose faculty_id is passed as the argument"""
	try:
		url="http://www.iitr.ac.in/"+cmsdb.query("select p.url from pages p, cocoon_pages c where c.page_id=p.page_id and c.name='"+fac_id+"'").dictresult()[0]['url']
	except:
		return ""
	return url
#def add_columns(
