from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.http import JsonResponse
from models import Bunk,TimeTable
from nucleus.models import RegisteredCourse,Student
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json
import pdb
# Create your views here.
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
     if request.method == 'POST':
       try:
        json_data = json.loads(request.body)
        for i in range(5):
          print day(i)
          dayData = json_data['%d'%i]
          for j in range(10):
            TimeTable.objects.create(student=student,day=day(i),subject=dayData['%d'%j]['subCode'],class_type=dayData['%d'%j]['classType'],time=times(j))
            print times(j)
            print dayData['%d'%j]['subCode'],dayData['%d'%j]['classType']

       except KeyError:
          return HttpResponseServerError("Malformed data!")
       return HttpResponse("Got json data")
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
