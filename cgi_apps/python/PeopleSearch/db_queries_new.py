#! /usr/bin/python
import os, sys
filepath = os.path.realpath(__file__)
channeli_path = '/'.join(filepath.split('/')[:3])+'/channel-i/'
sys.path.append(channeli_path)
services_table = "localnos"
try:
  from apache import override as settings
except:  
  import settings
from django.core.management import setup_environ
setup_environ(settings)

import db_connect
db = db_connect.connect_to_people_search()

import functions_new as functions

from api.model_constants import DEPARTMENT_CHOICES  
from nucleus.models import Branch,Person,PersonIdEnrollmentNoMap 
from facapp.constants import DESIGNATION_CHOICES
from facapp.models import Faculty

students = Person.objects.filter(passout_year=None)

def get_departments():
  """returns the dictionary departments for faculty"""
  department_list = []
  for department_choice in DEPARTMENT_CHOICES:
     department_list.append(
         { 'department_code': department_choice[0],
           'department_name': department_choice[1]
         }
     )    
  return department_list

def get_disciplines():
  """returns the dictionary of disciplines in Branch table"""
  branch_list=[]
  branches = Branch.objects.all()
  for branch in branches:
    branch_list.append(
        {'code':branch.code,
         'corresponds_to':branch.name+' ('+branch.graduation+')'
        }
    )
  return branch_list

def get_services():
	"""returns dictionary of different services from localnos table of test db"""
	services=db.query("select distinct(trim(type)) as type from localnos where type not in ('SCHOOLS AND COLLEGES','SELECTED LOCAL NOS.')")
	services=services.dictresult()
	return services

def get_fac_posts():
  """Returns dictionary of different faculty posts from post_mapping table of facappn db."""
  fac_posts_list=[]
  for designation_choice in DESIGNATION_CHOICES:
    fac_posts_list.append(
        {'post': designation_choice[0],
         'post_name': designation_choice[1]
         },
    )
  return fac_posts_list

def student_name_query(name):
  """Function to query by name in student table. Argument required is name only"""
  students = Person.objects.filter(passout_year=None)
  students = students.filter(name__icontains = name)
  result = []
  for student in students:
     pi_maps = PersonIdEnrollmentNoMap.objects.filter(enrollment_no = student.user.username)
     result.append({
      'count': '1',
      'course':student.semester,
      'degree':student.branch.degree,
      'deptt': student.branch.code,
      'enrollment_no': student.user.username,
      'name': student.name,
      'person_id': pi_maps[0].person_id if pi_maps.exists() else ''
    })
  return result

def faculty_name_query(name):
  """Function to query by name in faculty table.Requires name as argument""" 
  faculties = Faculty.objects.all()
  faculties = faculties.filter(name__icontains = name)
  result = []
  for faculty in faculties:
    result.append({
      'count': 1,
      'department_code': '',
      'deptt': faculty.department,
      'faculty_id': faculty.user.username,
      'name': faculty.name,
      'post_name': dict(DESIGNATION_CHOICES).get(faculty.designation,'')
    })
  return result

def services_name_query(name):
	"""Function to query by name in services table.Requires name as argument"""
	splitted_names=functions.split_the_name(name)
	result=[]
	query="select * from "+services_table+" where name is not null"
	for part in splitted_names:
		query=query+" and name ilike '%"+part+"%'"
	return db.query(query).dictresult()

def contact_num_query(contact_num):
    """Search  by contact number in all the db.Requires contact number as argument"""
    result=[]
    new_query=db.query("select * from "+services_table+" where contact_num ilike '%"+contact_num+"%'")
    result.extend(new_query.dictresult())
    result=functions.sort_query(result,contact_num)
    return result

"""def person_id_query(telnet_id):"""

def run_query_on_test(query):
	"""runs the passed query on the test db.it returns the list of dictionary results"""
	res=db.query(query)
	res=res.dictresult()
	return res

def adv_services(srch_str,serv_data):
	"""Handles the advanced services query if a selelction is made on the drop down menu of services tab"""
	if srch_str=="":
		return run_query_on_test("select * from localnos where type ='"+serv_data['name']+"'")
	que="select * from localnos where type='"+serv_data['name']+"' and name ilike '%"+srch_str+"%'"
	return db.query(que).dictresult()

def get_fac_url(fac_id):
	"""Returns the url of the faculty whose faculty_id is passed as the argument"""
	try:
		url="http://www.iitr.ac.in/"+cmsdb.query("select p.url from pages p, cocoon_pages c where c.page_id=p.page_id and c.name='"+fac_id+"'").dictresult()[0]['url']
	except:
		return ""
	return url

"""def assign_deptts(list)"""

def exact_id_query(Id):
  """searches for the exact id in person_extended and faculty"""
  a = PersonIdEnrollmentNoMap.objects.filter(person_id=Id)
  output = []
  if len(a)>0:
    b = students.filter(user__username = a[0].enrollment_no)
    c = Branch.objects.filter(code = b[0].branch_id)
    output =     ({'fac':[],
                   'serv':{},
                   'stud':[{'course':1,
                            'degree':c[0].degree,
                            'deptt':c[0].code,
                            'enrollment_no':a[0].enrollment_no,
                            'name':b[0].name ,
                            'person_id':Id}]})
  else :
    output =     ({'fac':[],
                   'serv':{},
                   'stud':[]})
  return output


def adv_faculty(srch_str,fac_data):
  """handles the advanced faculty query if a selection is made on the drop down menu of faculty tab.returns the dictionary containing the query result."""
  faculties = Faculty.objects.all()
  if srch_str != "":
    faculties = faculties.filter(name__icontains = srch_str)
  if fac_data['dept'] != "null":
    faculties = faculties.filter(department = fac_data['dept'])
  if fac_data['post'] != "null":
    faculties = faculties.filter(designation = fac_data['post'])
  result = []
  for faculty in faculties:
    result.append({
      'count': 1,
      'department_code': '',
      'deptt': faculty.department,
      'faculty_id': faculty.user.username,
      'name': faculty.name,
      'post_name': dict(DESIGNATION_CHOICES)[faculty.designation]
    })
  return result

def adv_student(srch_str,stud_data):
  """handles the advanced faculty query if a selection is made on the drop down menu of faculty tab.returns the dictionary containing the query result."""
  students = Person.objects.filter(passout_year=None)
  if srch_str != "":
    students = students.filter(name__icontains = srch_str)
  if stud_data['dept'] != "null":
    students = students.filter(branch__code = stud_data['dept'])
  if stud_data['year'] != "null":
    semester_list = ['UG%s0', 'UG%s1','PG%s0', 'PG%s1', 'PHD%s0', 'PHD%s1']
    semester_list = map(lambda s:s%stud_data['year'], semester_list)
    students = students.filter(semester__in = semester_list)
  if stud_data['prog'] != "null":
    prog = ({'1':'UG','2':'PG','3':'PHD'})[stud_data['prog']]
    students = students.filter(branch__graduation = prog)
  result = []
  for student in students:
     pi_maps = PersonIdEnrollmentNoMap.objects.filter(enrollment_no = student.user.username)
     result.append({
      'count': '1',
      'course':student.semester,
      'degree':student.branch.degree,
      'deptt': student.branch.code,
      'enrollment_no': student.user.username,
      'name': student.name,
      'person_id': pi_maps[0].person_id if pi_maps.exists() else ''
    })
  return result


