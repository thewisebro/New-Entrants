from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.http import JsonResponse
from models import Bunk,TimeTable
from nucleus.models import RegisteredCourse,Student,User
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json
import pdb
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
from nucleus.forms import LoginForm
from feeds.models import Feed
from utilities.models import UserSession
import logging
logger = logging.getLogger('channel-i_logger')
# Create your views here.
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
#import ipdb;ipdb.set_trace()
   sessionid=request.META.get('HTTP_SESSION_KEY')
 try:
   session = Session.objects.get(session_key=request.META.get('HTTP_SESSION_KEY'))
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
  result = {"success":"NO","_name":"","info":"","session_key":""}
  print request.method
  username = request.POST.get('username')
  password = request.POST.get('password')
  print username
  print password
  user = User.objects.get_or_none(username=username)
#  import ipdb;ipdb.set_trace()
  if not user:
    result['success'] = "NO"
  elif user.check_password(password):
# make_user_login(request,user)
    print user
    result['info'] = user.info.encode('utf-8')
    result['_name'] = user.name.encode('utf-8')
    result['success'] = "YES"
    result['session_key'] = make_user_login(request,user)
  else:
    result['success'] = "USER NO"
#response = HttpResponse(result)
# for key, value in HEADERS.iteritems():
#   result[key] = value
  c.append(result)
  print c
  return HttpResponse(c)


def bunkometer(request):
  return HttpResponse('So, started with bunkometer django part!')
def getSubjects(request,username):
  try:
    student = Student.objects.get(user__username=username)
    registeredCourses = []
    registeredCourses = RegisteredCourse.objects.filter(student = student)
    subData={}
    #nos -> number of subjects
    subData['nos'] = len(registeredCourses)
    for i in range(len(registeredCourses)):
       subData['sub%d'%(i+1)] = registeredCourses[i].course.code
       subData['sub%d_fullForm'%(i+1)] = registeredCourses[i].course.name
  except ObjectDoesNotExist:
    return JsonResponse({'nos':0 , 'error':'Object doesn\'t exist.'})
  return JsonResponse(subData)

def getBunks(request,username):
  try:
    student = Student.objects.get(user__username=username)
    bunks = Bunk.objects.filter(student=student)
    jsonObj = {}
    individual={}
    jsonObj['nos'] = len(bunks)
    for i in range(len(bunks)):
      individual={}
      individual['lec'] = bunks[i].lec_bunk
      individual['tut'] = bunks[i].tut_bunk
      individual['prac'] = bunks[i].prac_bunk
      jsonObj[bunks[i].subject] = individual
  except ObjectDoesNotExist:
    return JsonResponse({'nos':0,'error':'Object doesn\'t exist.'})
  return JsonResponse(jsonObj)

def day(x):
  if x is 0:
    return 'Mon'
  if x is 1:
    return 'Tues'
  if x is 2:
    return 'Wed'
  if x is 3:
    return 'Thurs'
  if x is 4:
    return 'Fri'
  return 'Unknown'


def times(x):
  if x is 0:
    return '8-9'
  elif x is 1:
    return '9-10'
  elif x is 2:
    return '10-11'
  elif x is 3:
    return '11-12'
  elif x is 4:
    return '12-1'
  elif x is 5:
    return '1-2'
  elif x is 6:
    return '2-3'
  elif x is 7:
    return '3-4'
  elif x is 8:
    return '4-5'
  elif x is 9:
    return '5-6'
  return 'Invalid time'


@csrf_exempt
def saveTimeTable(request,username):
   try:
     student = Student.objects.get(user__username=username)
     TimeTable.objects.filter(student__user__username=username).delete()
     c=[]
     ans = {'success':"NO"}
     if request.method == 'POST':
       result = check_session(request)
       if result['msg']=='YES':
         try:
          json_data = json.loads(request.body)
          for i in range(len(json_data)):
            day = json_data[i]['day']
            sche = json_data[i]['schedule']
            for j in range(len(sche)):
              time = sche[j]['time']
              cell = sche[j]['cell']
              cell['courseCode']
              TimeTable.objects.create(student=student,day=i,course_code=cell['courseCode'],course_name = cell['courseName'],class_type=cell['classType'],bunk=cell['bunk'],time=time)
          for i in range(5):
            print day(i)
            dayData = json_data['%d'%i]
            for j in range(10):
              TimeTable.objects.create(student=student,day=i,course_code=dayData['%d'%j]['courseCode'],class_type=dayData['%d'%j]['classType'],time=j)
              print times(j)
              print dayData['%d'%j]['subCode'],dayData['%d'%j]['classType']
              ans['success']="YES"
              c.append(ans)
         except KeyError:
            return HttpResponseServerError("Malformed data!")
         return HttpResponse(c)
     else:
       return HttpResponse(c)
   except ObjectDoesNotExist:
      return HttpResponse('Student doesn\'t exist.')


@csrf_exempt
def saveBunks(request,username):
  try:
    student = Student.objects.get(user__username=username)
    Bunk.objects.filter(student=student).delete()
    jsondata = json.loads(request.body)
    print jsondata
    subjects = jsondata.keys()
    print subjects
    for sub in subjects:
      Bunk.objects.create(student=student,subject=sub,lec_bunk=jsondata[sub]['lec'],tut_bunk=jsondata[sub]['tut'],prac_bunk=jsondata[sub]['prac'])
  except (ObjectDoesNotExist,KeyError):
    return HttpResponse("Student %s not found"%username)
  return HttpResponse('Saved the bunks.')

def getTimeTable(request,username):
  try:
    student = Student.objects.get(user__username=username)
    json = {}
    time_table = TimeTable.objects.filter(student=student)
#print time_table
    for i in range(5):
      day_schedule={}
      for j in range(10):
        cell = time_table.get(day=day(i),time=times(j)) 
        day_schedule['%d'%j] = {'code':cell.subject,'class_type':cell.class_type}
      json['%d'%i] = day_schedule
    for i in range(5):
      for j in range(10):  
        cell = json['%d'%i]['%d'%j]
        print cell['code'],cell['class_type']
  except (ObjectDoesNotExist): 
    return HttpResponse('Invalid student %s, or KeyError in timetable.'%username)
  return JsonResponse(json)
