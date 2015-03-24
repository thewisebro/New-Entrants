from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.http import JsonResponse
from models import Bunk
from nucleus.models import RegisteredCourse,Student
from django.db.models.base import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json
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
def receive(request,username):
  if request.method == 'POST':
      try:
        json_data = json.loads(request.body)
        for i in range(5):
          print day(i)
          dayData = json_data['%d'%i]
          for j in range(10):
            print times(j)
            print dayData['%d'%j]['subCode'],dayData['%d'%j]['classType']

      except KeyError:
        return HttpResponseServerError("Malformed data!")
      return HttpResponse("Got json data")
