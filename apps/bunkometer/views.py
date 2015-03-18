from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from models import Bunk
from nucleus.models import RegisteredCourse,Student
# Create your views here.
def bunkometer(request):
  return HttpResponse('So, started with bunkometer django part!')
def getSubjects(request,username):
  student = Student.objects.get(user__username=username)
  registeredCourses = []
  registeredCourses = RegisteredCourse.objects.filter(student = student)
  
  subData={}
  #nos -> number of subjects
  subData['nos'] = len(registeredCourses)
  for i in range(len(registeredCourses)):
    subData['sub%d'%(i+1)] = registeredCourses[i].course.code
    subData['sub%d_fullform'%(i+1)] = registeredCourses[i].course.name
  return JsonResponse(subData)
