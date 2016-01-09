# Create your views here.
from nucleus.models import Student, Faculty, User
from groups.models import GroupInfo, Group
from peoplesearch.models import Services
from django.http import HttpResponse

from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import check_password, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
#from settings import SESSION_COOKIE_NAME
#
from nucleus.forms import LoginForm
from nucleus.utils import get_webmail_account, check_webmail_login
from feeds.models import Feed
from utilities.models import UserSession
import crypt
import json
from hashlib import sha1

import logging
logger = logging.getLogger('channel-i_logger')

def return_details(request):
  c=[]
  result = {"msg":"NO","_name":"","info":"","session_variable":"", "enrollment_no":""}
  username = request.GET.get("username")
  user = User.objects.get_or_none(username=username)
  if not user:
    webmail_account = get_webmail_account(username)
    if webmail_account:
      username = webmail_account.user.username
      user = webmail_account.user
  if user:
    result["msg"] = "YES"
    result["_name"] = user.name.encode('utf-8')
    result["info"] = user.info.encode('utf-8')
    result["enrollment_no"] = user.username.encode('utf-8')
  c.append(result)
  return HttpResponse(c)

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
  result = {"msg":"NO","_name":"","info":"", "session_variable":"", "enrollment_no":""}

  if request.method == "POST":
    sessionid=request.POST.get("session_key","")
#    sessionid = request.COOKIES.get(SESSION_COOKIE_NAME)
#csrftoken = request.POST.get('X_token')
    try:
      session = Session.objects.get(session_key=sessionid)
      print sessionid
      current_user_id = session.get_decoded().get('_auth_user_id')
      print current_user_id
      user = User.objects.get_or_none(pk=current_user_id)
      print user
      if user:
        result["info"] = user.info.encode('utf-8')
        print user.info
        result["_name"] = user.name.encode('utf-8')
        result["msg"] = "YES"
        result["session_variable"] = sessionid.encode('utf-8')
        result["enrollment_no"] = user.username.encode('utf-8')
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
  result = {"msg":"NO","_name":"","info":"","session_variable":"","enrollment_no":""}
  username = request.POST.get('username')
  password = request.POST.get('password')
  print username
  print password
  user = User.objects.get_or_none(username=username)
  if not user:
    webmail_account = get_webmail_account(username)
    if webmail_account:
      username = webmail_account.user.username
      user = webmail_account.user
      if check_webmail_login(webmail_account.webmail_id if webmail_account else\
                                   username, password): 
        result["info"] = user.info.encode('utf-8')
        result["_name"] = user.name.encode('utf-8')
        result["msg"] = "YES"
        result["session_variable"] = make_user_login(request,user)
        result["enrollment_no"] = user.username.encode('utf-8')
      else:
        result["msg"] = "NO"
    else:  
      result["msg"] = "NO"
  elif user.check_password(password):
# make_user_login(request,user)
    result["info"] = user.info.encode('utf-8')
    result["_name"] = user.name.encode('utf-8')
    result["msg"] = "YES"
    result["session_variable"] = make_user_login(request,user)
    result["enrollment_no"] = user.username.encode('utf-8')
  else:
    result["msg"] = "NO"
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
  result = {"msg":"","_name":"","info":"","session_variable":""}

  if request.method == "POST":
    sessionid = request.POST.get("session_key")
    try:
      session = Session.objects.get(session_key=sessionid)
      session.delete()
      result["msg"] = "OK"
    except:
      result["msg"] = "FAILURE"
  else:
    result["msg"] = "FAILURE"
#  response = HttpResponse(json.dumps(result), contenttype='application/json')
#  for key, value in HEADERS.iteritems():
#    response[key] = value
  c.append(result)
  return HttpResponse(c)

def base(request):
  context={}
  return render(request, 'peoplesearch/htmlcode_new.html', context)

def index(request):
  srch_str = request.GET.get('name','Manohar')
  branch = request.GET.get('branch','')
  year = request.GET.get('year','')
  role = request.GET.get('role','stud')
  faculty_department = request.GET.get('faculty_department','')
  faculty_designation = request.GET.get('faculty_designation','')
  services_list = request.GET.get('services_list','')
  groups_list = request.GET.get('groups_list','')
  counter = request.GET.get('counter',0)
  session = request.GET.get('session',0)
  source = request.GET.get('source','')
#  flag=0
  count=0
  count_stud=0
  count_fac=0
  count_serv=0
  count_groups=0
  i=0
  result={"role":role.encode('utf-8'),"data":[],"count":[]}
  result["data"] = {"stud":[],"fac":[],"serv":[],"groups":[]}
  c=[]
#check session
#student search
  if role == "stud":
    students = Student.objects.filter(~Q(passout_year = 0), passout_year__isnull = True)
    a=2*int('0'+year)
    b=2*int('0'+year)-1
    if srch_str != "":
      students = students.filter(user__name__icontains=srch_str)
    if branch != "":
      students = students.filter(branch__code__icontains=branch)
    if year != "":
      students = students.filter(Q(semester_no=a)|Q(semester_no=b))
    count = students.count()
    result["count"] = count
    if source == "android":
      students = students[counter:counter+10]
    for student in students:
      if student.bhawan is None:
        student.bhawan = ""
      result["data"]["stud"].append(
                {
                'name':student.user.name.encode('utf-8'),
                'enrollment_no':student.user.username.encode('utf-8'),
                'branch':student.branch.code.encode('utf-8'),
                'year':int((student.semester_no+1)/2),
                'bhawan':student.bhawan.encode('utf-8'),
                'room':student.room_no.encode('utf-8'),
                })
    if source == "ajax":
      return render(request, 'peoplesearch/results_ajax.html', result)
    elif source == "web":
      return render(request, 'peoplesearch/results_extension.html', result)
    c.append(result)
    return HttpResponse(c)

#faculty search
  if role == "fac":
    faculties = Faculty.objects.all()
    if srch_str != "":
      faculties = faculties.filter(user__name__icontains=srch_str)
    if faculty_department != "":
      faculties = faculties.filter(department__icontains=faculty_department)
    if faculty_designation != "":
      faculties = faculties.filter(designation__icontains=faculty_designation)
    count = faculties.count()
    result["count"] = count
    if source == "android":
      faculties = faculties[counter:counter+10]
    for faculty in faculties:
      result["data"]["fac"].append({
            'username':faculty.user.username.encode('utf-8'),
            'name':faculty.user.name.encode('utf-8'),
            'department':faculty.department.encode('utf-8'),
            'designation':faculty.designation.encode('utf-8'),
            })
    if source == "ajax":
      return render(request, 'peoplesearch/results_ajax.html', result)
    elif source == "web":
      return render(request, 'peoplesearch/results_extension.html', result)
    c.append(result)
    return HttpResponse(c)

#services search
  if role == "serv":
    services = Services.objects.all()
    if srch_str != "":
      services = services.filter(name__icontains = srch_str)
    if services_list != "":
      services = services.filter(service__icontains = services_list)
    count = services.count()
    result["count"] = count
    if source == "android":
      services = services[counter:counter+10]
    for service in services:
      result["data"]["serv"].append({
            'name':service.name.encode('utf-8'),
            'office_no':service.office_no.encode('utf-8'),
            'service':service.service.encode('utf-8'),
            })
    if source == "ajax":
      return render(request, 'peoplesearch/results_ajax.html', result)
    elif source == "web":
      return render(request, 'peoplesearch/results_extension.html', result)
    c.append(result)
    return HttpResponse(c)

#group search
  if role == "groups":
    groups = GroupInfo.objects.all()
    if srch_str != "":
      groups = groups.filter(group__name__icontains = srch_str)
    if groups_list != "":
      groups = groups.filter(group__user__username__icontains = groups_list)
    count = groups.count()
    result["count"]=count
    groups = groups[counter:counter+10]
    for group in groups:
        result["data"]["groups"].append({
            'name':group.group.user.username.encode('utf-8'),
            'phone-no':group.phone_no.encode('utf-8'),
            'email':group.email.encode('utf-8'),
            })
    c.append(result)
    return HttpResponse(c)

#all search
  if role == "all":
    if srch_str != "":
      students = Student.objects.filter(~Q(passout_year = 0), passout_year__isnull = True)
      students = students.filter(user__name__icontains = srch_str)
      count_stud = students.count()
      faculties = Faculty.objects.all()
      faculties = faculties.filter(user__name__icontains = srch_str)
      count_fac = faculties.count()
      services = Services.objects.all()
      services = services.filter(name__icontains = srch_str)
      count_serv = services.count()
      if source == "android":
        groups = GroupInfo.objects.all()
        groups = groups.filter(group__name__icontains = srch_str)
        count_groups = groups.count()
      count = count_stud + count_fac + count_serv + count_groups
      result["count"] = count
      for student in students:
        if student.bhawan is None:
          student.bhawan = ""
        result["data"]["stud"].append(
              {
             'name':student.user.name.encode('utf-8') ,
             'enrollment_no':student.user.username.encode('utf-8') ,
             'branch':student.branch.code.encode('utf-8'),
             'year':int((student.semester_no+1)/2),
             'bhawan':student.bhawan.encode('utf-8'),
             'room':student.room_no.encode('utf-8'),
             })
        i = i+1
        if i == 20*counter and source == "android":
          result["data"] = []
        if i == 20*(int('0'+counter)+1) and source == "android":
          c.append(result)
          return HttpResponse(c)

      for faculty in faculties:
        result["data"]["fac"].append({
            'name':faculty.user.name.encode('utf-8'),
            'username':faculty.user.username.encode('utf-8'),
            'department':faculty.department.encode('utf-8'),
            'designation':faculty.designation.encode('utf-8'),
            'office-no':faculty.user.contact_no.encode('utf-8')
            })
        i = i+1
        if i == 20*counter and source == "android":
          result["data"] = []
        if i == 20*(int('0'+counter)+1) and source == "android":
          c.append(result)
          return HttpResponse(c)

      for service in services:
        result["data"]["serv"].append({
          'name':service.name.encode('utf-8'),
          'office_no':service.office_no.encode('utf-8'),
          'service':service.service.encode('utf-8')
          })
        i = i+1
        if i == 20*counter and source == "android":
          result["data"] = []
        if i == 20*(int('0'+counter)+1) and source == "android":
          c.append(result)
          return HttpResponse(c)

      if source == "android":
        for group in groups:
          result["data"]["groups"].append({
          'name':group.group.user.username.encode('utf-8'),
          'phone-no':group.phone_no.encode('utf-8'),
          'email':group.email.encode('utf-8'),
          })
          i = i+1
          if i == 20*counter or i == count/20*20 and source == "android":
            result["data"] = []
          if i == 20*(int('0'+counter)+1) and source == "android":
            c.append(result)
            return HttpResponse(c)
      else:
        i = i+count_groups
      if source == "web":
        return render(request, 'peoplesearch/results_extension.html', result)
      elif source == "ajax":
        return render(request, 'peoplesearch/results_ajax.html', result)
      c.append(result)
      return HttpResponse(c)

