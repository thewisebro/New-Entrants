from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from models import Bunk
# Create your views here.
def bunkometer(request):
  return HttpResponse('So, started with bunkometer django part!')
def getSubjects(request,username):
  details = Bunk.objects.filter(rollNumber=username)
  subData={}
  #nos -> number of subjects
  subData['nos'] = len(details)
  for i in range(len(details)):
    subData['sub%d'%(i+1)] = details[i].subject
  return JsonResponse(subData)
