# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from facapp.models import *
from django.shortcuts import render
from facapp import sectionData
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
  data = {}
#   if 'title' in request.POST:
#     title = request.POST['title']
#     value = request.POST['content']
#     s = Section.objects.get(title=title)
#     s.content = value
#     s.save()
#     return HttpResponse(value)
# #   return HttpResponse(data.titles)
#   sections = Section.objects.order_by('priority')
#   titlesList = sectionData.titles
#   data = {"sections" : sections, "titles_list" : titlesList}
  return render(request, 'facapp/index.html', data)

@csrf_exempt
def sendFields(request, title):
  sections = sectionData.data
  for section in sections:
    if section[0][1] == title:
#       print section[2][1]
      sendIt = ""
      for fields in section[2][1]:
        sendIt += fields[0] + ":" + fields[1] + ","
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
    user = request.user
    print user
    p = Faculty.objects.get(user=user)
    s = Section.objects.create(title  = title, professor = p, priority = priority, content = content)
    return HttpResponse('created new section instance')
  return HttpResponse('no post request detected')

@csrf_exempt
def setPriority(request):
  if 'priority' in request.POST and request.user!='NULL' :
    data = request.POST['priority']
    professor = request.user
    titles = data.split(',')
    for idx,title in enumerate(titles):
      section = Section.objects.get(title = title, professor = professor)
      section.priority = idx + 1
      section.save()
      print section.priority
    # try:
    # print section.priority
    # except Section.DoesNotExist:
    #   # no employee found
    # except Section.MultipleObjectsReturned:
    #   # what to do if multiple employees have been returned?
    return HttpResponse('priority set')
  else:
    HttpResponse('something is not right.')
