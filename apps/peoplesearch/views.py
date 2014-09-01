# Create your views here.
from nucleus.models import Student, Faculty, User
from groups.models import GroupInfo
from peoplesearch.models import Services
from django.http import HttpResponse

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import check_password, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
#from settings import SESSION_COOKIE_NAME
#
from nucleus.forms import LoginForm
from feeds.models import Feed
from utilities.models import UserSession
import crypt
import json
from hashlib import sha1

import logging
logger = logging.getLogger('channel-i_logger')

def make_user_login(request,user):
  user.backend='django.contrib.auth.backends.ModelBackend'
  auth_login(request, user)
  session_key = request.session._get_session_key()
  user_session = UserSession.objects.create(user=user, session_key=session_key)
#user_session.ip = get_client_ip(request)
# user_session.browser = request.user_agent.browser.family
# user_session.os = request.user_agent.os.family
  user_session.save()
  return session_key.encode('utf-8')

@csrf_exempt
def check_session(request):
  HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Max-Age': 1000,
    'Access-Control-Allow-Headers': 'x-Requested-With'}

  c=[]
  result = {"msg":"NO","_name":"","info":"", "session_variable":""}

  if request.method == "POST":
    sessionid=request.POST.get("session_key","")
#    sessionid = request.COOKIES.get(SESSION_COOKIE_NAME)
#csrftoken = request.POST.get('X_token')
    try:
      session = Session.objects.get(session_key=sessionid)
      current_user_id = session.get_decoded().get('_auth_user_id')
      user = User.objects.get_or_none(pk=current_user_id)
      if user:
        result["info"] = user.info()
        result["_name"] = user.name
        result["msg"] = "YES"
        result["session_variable"] = session
    except Exception as e:
      pass
      logger.info("nucleus -> peoplesearch -> check_session: , error: "+ str(e))

#  response = HttpResponse(json.dumps(result), contenttype='application/json')
  c.append(result)
#  for key, value in HEADERS.iteritems():
#    response[key] = value
  return HttpResponse(c)

@csrf_exempt
def channeli_login(request):
  HEADERS = {
     'Access-Control-Allow-Origin': '*',
     'Access-Control-Allow-Methods': 'POST',
     'Access-Control-Max-Age': 1000,
     'Access-Control-Allow-Headers': 'x-Requested-With'}

  c=[]
  result = {"msg":"NO","_name":"","info":"","session_variable":""}
  print request.method
  username = request.POST.get('username')
  password = request.POST.get('password')
  print username
  print password
  user = User.objects.get_or_none(username=username)
  if not user:
    result['msg'] = "NO"
  elif user.check_password(password):
# make_user_login(request,user)
    result['info'] = user.info.encode('utf-8')
    result['_name'] = user.name.encode('utf-8')
    result['msg'] = "YES"
    result['session_variable'] = make_user_login(request,user)
  else:
    result['msg'] = "USER NO"
#response = HttpResponse(result)
# for key, value in HEADERS.iteritems():
#   result[key] = value
  c.append(result)
  return HttpResponse(c)

# webmail login

@csrf_exempt
def logout_user(request):
  HEADERS = {
   'Access-Control-Allow-Origin': '*',
   'Access-Control-Allow-Methods': 'POST',
   'Access-Control-Max-Age': 1000,
   'Access-Control-Allow-Headers': 'x-Requested-With'}

  c=[]
  result = {'msg':''}

  if request.method == "POST":
    sessionid = request.POST.get("session_key")
    try:
      session = UserSession.objects.get(session_key=sessionid)
      session.delete()
      result['msg'] = "OK"
    except:
      result['msg'] = "FAILURE"
  else:
    result['msg'] = "FAILURE"
#  response = HttpResponse(json.dumps(result), contenttype='application/json')
#  for key, value in HEADERS.iteritems():
#    response[key] = value
  c.append(result)
  return HttpResponse(c)

def index(request):
  srch_str = request.GET.get('name','Manohar')
  branch = request.GET.get('branch','')
  year = request.GET.get('year','')
  role = request.GET.get('role','Students')
  faculty_department = request.GET.get('faculty_department','')
  faculty_designation = request.GET.get('faculty_designation','')
  services_list = request.GET.get('services_list','')
  groups_list = request.GET.get('groups_list','')
  counter = request.GET.get('counter',0)
  session = request.GET.get('session',0)
  flag=0
  temp=0
  temp_stu=0
  temp_fac=0
  temp_ser=0
  temp_gro=0
  i=0
  result={"role":role,"data":[],"temp":0}
  c=[]
#check session
#student search
  if role == "Students":
    students = Student.objects.all()
    a=2*int('0'+year)
    b=2*int('0'+year)+1
    if srch_str != "":
      flag = 10  #some random no
      students = students.filter(user__name__icontains=srch_str)
    if branch != "":
      flag = flag+1
      students = students.filter(branch__code__icontains=branch)
    if year != "":
      flag = flag+1
      students = students.filter(semester_no=a)
      students = students.filter(semester_no=b)
    if flag == 1 or flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = students.count()
      result["temp"] = temp
      for student in students:
        result["data"].append(
              {
             'name':student.user.name.encode('utf-8') ,
             'enrollment_no':student.user.username.encode('utf-8') ,
             'branch':student.branch.code.encode('utf-8'),
             'year':int((student.semester_no+1)/2),
             'bhawan':student.bhawan.encode('utf-8'),
             'room':student.room_no.encode('utf-8'),
             })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#faculty search
  if role == "Faculties":
    faculties = Faculty.objects.all()
    if srch_str != "":
      flag = 1
      faculties = faculties.filter(user__name__icontains=srch_str)
    if faculty_department != "":
      faculties = faculties.filter(department__icontains=faculty_department)
    if faculty_designation != "":
      faculties = faculties.filter(designation__icontains=faculty_designation)
    if flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = faculties.count()
      result["temp"]=temp
      for faculty in faculties:
        result["data"].append({
            'name':faculty.user.name.encode('utf-8'),
            'username':faculty.user.username.encode('utf-8'),
            'department':faculty.department.encode('utf-8'),
            'designation':faculty.designation.encode('utf-8'),
            'office-no':faculty.user.contact_no.encode('utf-8'),
            })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#services search
  if role == "Services":
    services = Services.objects.all()
    if srch_str != "":
      flag = 1
      services = services.filter(name__icontains = srch_str)
    if services_list != "":
      services = services.filter(service_icontains = services_list)
    if flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = services.count()
      result["temp"]=temp
      for service in services:
        result["data"].append({
            'name':service.name.encode('utf-8'),
            'office_no':service.office_no.encode('utf-8'),
            'service':service.service.encode('utf-8'),
            })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#group search
  if role == "Groups":
    groups = GroupInfo.objects.all()
    if srch_str != "":
      flag = 1
      groups = groups.filter(group__name__icontains = srch_str)
    if groups_list != "":
      groups = groups.filter(group__user__username__icontains = groups_list)
    if flag == 0:
      c.append(result)
      return HttpResponse(c)
    else:
      temp = groups.count()
      result["temp"] = temp
      for group in groups:
        result["data"].append({
            'name':group.group.user.username.encode('utf-8'),
            'phone-no':group.phone_no.encode('utf-8'),
            'email':group.email.encode('utf-8'),
            })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)
      c.append(result)
      return HttpResponse(c)

#all search
  if role == "All":
    result["data"] = {"Students":[],"Faculties":[],"Services":[],"Groups":[]}
    if srch_str != "":
      students = Student.objects.all()
      students = students.filter(user__name__icontains = srch_str)
      temp_stu = students.count()
      faculties = Faculty.objects.all()
      faculties = faculties.filter(user__name__icontains = srch_str)
      temp_fac = faculties.count()
      services = Services.objects.all()
      services = services.filter(name__icontains = srch_str)
      temp_ser = services.count()
      groups = GroupInfo.objects.all()
      groups = groups.filter(group__name__icontains = srch_str)
      temp_gro = groups.count()
      temp = temp_stu +temp_fac + temp_ser + temp_gro
      result["temp"] = temp
      for student in students:
        result["data"]["Students"].append(
              {
             'name':student.user.name.encode('utf-8') ,
             'enrollment_no':student.user.username.encode('utf-8') ,
             'branch':student.branch.code.encode('utf-8'),
             'year':int((student.semester_no+1)/2),
             'bhawan':student.bhawan.encode('utf-8'),
             'room':student.room_no.encode('utf-8'),
             })
        i = i+1
        if i == 20*counter:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      for faculty in faculties:
        result["data"]["Faculties"].append({
            'name':faculty.user.name.encode('utf-8'),
            'username':faculty.user.username.encode('utf-8'),
            'department':faculty.department.encode('utf-8'),
            'designation':faculty.designation.encode('utf-8'),
            'office-no':faculty.user.contact_no.encode('utf-8')
            })
        i = i+1
        if i == 20*counter:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      for service in services:
        result["data"]["Services"].append({
          'name':service.name.encode('utf-8'),
          'office_no':service.office_no.encode('utf-8'),
          'service':service.service.encode('utf-8')
          })
        i = i+1
        if i == 20*counter:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      for group in groups:
        result["data"]["Groups"].append({
          'name':group.group.user.username.encode('utf-8'),
          'phone-no':group.phone_no.encode('utf-8'),
          'email':group.email.encode('utf-8'),
        })
        i = i+1
        if i == 20*counter or i == temp/20*20:
          result["data"] = []
        if i == 20*(int('0'+counter)+1):
          c.append(result)
          return HttpResponse(c)

      c.append(result)
      return HttpResponse(c)
    else:
      c.append(result)
      return HttpResponse(c)

