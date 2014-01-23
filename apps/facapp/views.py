# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from facapp.models import *
from django.shortcuts import render

def home(request):
  return render(request, 'facapp/home.html')

