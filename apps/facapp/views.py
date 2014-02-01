# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from facapp.models import *
from django.shortcuts import render
from facapp import data
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
  print "yess"
  if 'ckedit' in request.POST:
    show = request.POST["ckedit"]
    print "here"
    return HttpResponse(show)
#   return HttpResponse(data.titles)
  return render(request, 'facapp/home.html')

