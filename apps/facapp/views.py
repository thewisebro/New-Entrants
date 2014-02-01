# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from facapp.models import *
from django.shortcuts import render
from facapp import data

def home(request):
  if 'submit' in request.POST:
    return HttpResponse("hello there")
#   return HttpResponse(data.titles)
  return render(request, 'facapp/home.html')

