# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from facapp.models import *
from django.shortcuts import render
from facapp import sectionData
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
  print "yess"
  sections = Section.objects.all()
  titles_list = sectionData.titles
  data = {"sections" : sections, "titles_list" : titles_list}
  if 'title' in request.POST:
    title = request.POST['title']
    value = request.POST['content']
    s = Section.objects.get(title=title)
    s.content = value
    s.save()
    print "here"
    return HttpResponse(value)
#   return HttpResponse(data.titles)
  return render(request, 'facapp/home.html', data)

