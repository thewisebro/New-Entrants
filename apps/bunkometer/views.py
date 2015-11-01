from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.http import JsonResponse
from models import Bunk,TimeTable, Course
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
# c.append(result)
#  for key, value in HEADERS.iteritems():
#    response[key] = value
 return result

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
    result['success'] = "NO"
#response = HttpResponse(result)
# for key, value in HEADERS.iteritems():
#   result[key] = value
  c.append(result)
  print c
  return HttpResponse(c)


###################################################################

def bunkometer(request):
  return HttpResponse('So, started with bunkometer django part!')
def getRegisteredCourses(request,username):
  try:
    student = Student.objects.get(user__username=username)
    registeredCourses = []
    registeredCourses = RegisteredCourse.objects.filter(student = student)
    subData={}
    #nos -> number of subjects
    subData['nos'] = len(registeredCourses)
    courses = []
    for i in range(len(registeredCourses)):
       course = {}
       course['code'] = registeredCourses[i].course.code
       course['name'] = registeredCourses[i].course.name
       courses.append(course)
    subData['courses'] = courses
  except ObjectDoesNotExist:
    return JsonResponse({'nos':0 , 'courses' : [],'error':'Object doesn\'t exist.'})
  return JsonResponse(subData)

def getCourses(request, username):
  ans = {'nos': 0, 'courses': []}
  try:
    student = Student.objects.get(user__username = username)
    courses = Course.objects.filter(student = student)
    ans['nos'] = len(courses)
    for course in courses:
      json = {}
      json['code'] = course.course_code
      json['name'] = course.course_name
      ans['courses'].append(json)
    return JsonResponse(ans)
  except Exception as e:
    return JsonResponse(ans)

def getBunks(request,username):
  ans = {'success': 'NO', 'bunks': []}
  try:
    student = Student.objects.get(user__username=username)
    bunks = Bunk.objects.filter(student=student)
    for bunk in bunks:
      json = {}
      data = {}
      json['course'] = {}
      json['course']['code'] = bunk.course_code
      json['course']['name'] = Course.objects.get(student = student, course_code = bunk.course_code).course_name
      data['lec'] = bunk.lec_bunk
      data['lecTotal'] = bunk.lec_total
      data['tut'] = bunk.tut_bunk
      data['tutTotal'] = bunk.tut_total
      data['prac'] = bunk.prac_bunk
      data['pracTotal'] = bunk.prac_total
      json['bunk'] = data
      ans['bunks'].append(json)
    ans['success'] = 'YES'  
    return JsonResponse(ans)
  except Exception as e:
    return JsonResponse(ans)

@csrf_exempt
def saveTimeTable(request,username):
   ans = {'success':'NO'}
   try:
     student = Student.objects.get(user__username=username)
     TimeTable.objects.filter(student__user__username=username).delete()
     if request.method == 'POST':
       result = check_session(request)
       if result['msg']=='YES':
         try:
          json_data = json.loads(request.body)
          print len(json_data)
          for i in range(len(json_data)):
            day = json_data[i]['day']
            sche = json_data[i]['schedule']
            for j in range(len(sche)):
              time = sche[j]['time']
              cell = sche[j]['cell']
              print day, time, cell['courseCode']
              TimeTable.objects.create(student=student,day=i,course_code=cell['courseCode'],course_name = cell['courseName'],class_type=cell['classType'],bunk=cell['bunk'],time=time)
            ans['success'] = 'YES'
            ans['message'] = 'Successfully saved timetable to Cloud.'
          return JsonResponse(ans)
         except KeyError:
            ans['message'] = 'Failed because of Key Error.'
            return JsonResponse(ans)
       else:
         ans['message'] = 'UNAUTHORIZED'
         return JsonResponse(ans)
     else:
       ans['message'] = 'Failed: Not a POST request.'
       return JsonResponse(ans)
   except ObjectDoesNotExist:
      ans['message'] = 'Required student doesn\'t exist.'
      return JsonResponse(ans)


@csrf_exempt
def saveBunks(request,username):
  ans = {'success':'NO'}
  try:
    result = check_session(request)
    if result['msg']!='YES':
      ans['message'] = 'UNAUTHORIZED'
      return JsonResponse(ans)
    print 'bunks'
    student = Student.objects.get(user__username=username)
    Bunk.objects.filter(student__user__username=username).delete()
    bunksData = json.loads(request.body)
#print JsonResponse(bunksData) 
    for courses in bunksData:
       bunk = courses['bunk']
       course = courses['course']
       Bunk.objects.create(student = student, course_code = course['code'], lec_bunk = bunk['lec'], lec_total = bunk['lecTotal'], tut_bunk = bunk['tut'], tut_total = bunk['tutTotal'], prac_bunk = bunk['prac'], prac_total = bunk['pracTotal'])

  except (ObjectDoesNotExist,KeyError):
    ans['message'] = 'Failed: User doesn\'t exist OR Server error.'
    return JsonResponse(ans)
  ans['message'] = 'Successfully saved the bunks to cloud.'
  ans['success'] = 'YES'
  return JsonResponse(ans)

@csrf_exempt
def saveCourses(request, username):
  ans = {'success': 'NO'}
  try:
     result = check_session(request)
     if result['msg']!='YES':
      ans['message'] = 'UNAUTHORIZED'
      return JsonResponse(ans)
     print 'courses'
     courses = json.loads(request.body)
     print 'Courses number: ',len(courses)
     student = Student.objects.get(user__username = username)
     Course.objects.filter(student__user__username = username).delete()
     for course in courses:
        print course['code'], course['name']
        Course.objects.create(student = student, course_code = course['code'], course_name = course['name'])
     ans['success'] = 'YES'
     ans['message'] = 'Successfully saved courses to cloud.'
     return JsonResponse(ans)
  except Exception as e:
     ans['message'] = '%s (%s)' % (e.message, type(e))
     return JsonResponse(ans)

def getTimeTable(request,username):
  ans = {'success': 'NO', 'timetable':[]}
  try:
    student = Student.objects.get(user__username=username)
    time_table = TimeTable.objects.filter(student=student)
    data = [{}]*7
    for day in range(len(data)):
      json = {}
      json['day'] = day
      json['schedule'] = []
      data[day] = json
    for cell in time_table:
      print cell.time, cell.day, cell.course_name
      binderCellToTime = {}
      binderCellToTime['time'] = cell.time
      _cell = {}
      _cell['courseCode'] = cell.course_code
      _cell['courseName'] = cell.course_name
      _cell['classType'] = cell.class_type
      _cell['bunk'] = cell.bunk
      binderCellToTime['cell'] = _cell
      data[cell.day]['schedule'].append(binderCellToTime)
    ans['timetable'] = data
    ans['success'] = 'YES'
    return JsonResponse(ans)
  except Exception as e:
    ans['message'] = '%s (%s)'%(e.message, type(e))
    return JsonResponse(ans)
