# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from facapp.models import *
from django.shortcuts import render
from facapp import sectionData
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
  print "yess"
  if 'title' in request.POST:
    title = request.POST['title']
    value = request.POST['content']
    s = Section.objects.get(title=title)
    s.content = value
    s.save()
    print "here"
    return HttpResponse(value)
#   return HttpResponse(data.titles)
  sections = Section.objects.all()
  titlesList = sectionData.titles
  data = {"sections" : sections, "titles_list" : titlesList}
  return render(request, 'facapp/home.html', data)

@csrf_exempt
def sendFields(request, title):
  sections = sectionData.data
  print title
  for section in sections:
    if section[0][1] == title:
#       print section[2][1]
      print 'this is what is being sent'
#       sendIt = "{"
      sendIt = ""
      for fields in section[2][1]:
#         sendIt += ( fields[0] + " " )
#         sendIt += '"' + fields[0] + '" : "' + fields[1] + '",'
        sendIt += fields[0] + ":" + fields[1] + ","
#       sendIt += "}"
      print sendIt
#       return HttpResponse(section[2][1])
      return HttpResponse(sendIt)
  return HttpResponse('try using the others category if you want another title')

@csrf_exempt
def createSection(request):
  print "recieved"
  if 'title' in request.POST:
    title = request.POST['title']
    content = request.POST['content']
    priority = request.POST['priority']
    priority = int(priority)
    user = request.user
    p = Faculty.objects.get(user=user)
    print p
    s = Section.objects.create(title  = title, professor = p, priority = priority, content = content)
    return HttpResponse('created new section instance')
  return HttpResponse('no post request detected')
