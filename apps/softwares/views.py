import os
import urllib2
import urllib
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings
from softwares.models import Software
from constants import CATEGORIES, SOFTWARE_LOCATION, SOFTWARE_IDS

def browse(request, category=None, softwareid=None):
  try:
    software = Software.objects.get(pk=softwareid)
    return render(request,'softwares/eachsoft.html',
         {'software': software, 'query': software.soft_name},)
  except:
    raise Http404


def search(request):
  query = request.GET.get('q', '').lower()
  results = []
  if query:
    #TODO: use haystack search, profile vs 3 queries
    qset = (
              Q(soft_name__icontains=query) |
              Q(category__icontains=query) |
              Q(description__icontains=query)
           )
    results = Software.objects.filter(qset)
    soft_list = []
    cat_list = []
    desc_list = []
    for result in results:
      if query in result.soft_name.lower():
        soft_list.append(result)
      elif query in result.category.lower():
        cat_list.append(result)
      elif query in result.description.lower():
        desc_list.append(result)
    soft_list.sort(key=lambda software: software.date_added)
    cat_list.sort(key=lambda software: software.date_added)
    desc_list.sort(key=lambda software: software.date_added)
    result = soft_list + cat_list + desc_list
  else:
    result = None
  return render(request,'softwares/search.html',
              {'result': result, 'query': query})

def index(request, category=None, softwareid=None):
  top4 = {}
  softwares = {}
  soft_check = [] # to check whether a category of software exists or not
  for category in CATEGORIES:
    top4[category[0]] = Software.objects.filter(category=
                        category[0]).order_by('-download_count')[:4]
    if not softwareid:
      softwares[category[0]] = Software.objects.filter(category=
                              category[0]).order_by('-date_added')
      check = False
      for software in softwares[category[0]]:
        url = MEDIA_ROOT+str(software.soft_file)
        if os.path.exists(url):
          check = True
      soft_check.append(check)
      if not softwares:
        raise Http404
  data = zip(CATEGORIES,soft_check)
  return render(request,'softwares/index.html',{'data': data,
          'top4': top4,'softwares': softwares,})


def download_count(request, software_id):
  try:
    software = Software.objects.get(pk=int(software_id))
    if request.is_ajax() and request.method == 'POST':
      software.download_count = software.download_count + 1
      software.save()
      result = True
      data = json.dumps({'result':result})
      return HttpResponse(data,content_type='application/json')
  except:
    return HttpResponse('')

def index_linux(request):
  softwares = []
  check = True
  for software_id in SOFTWARE_IDS:
    try:
      software = Software.objects.get(pk=int(software_id))
      url = MEDIA_ROOT+str(software.soft_file)
      if not os.path.exists(url):
        check = False
      softwares.append(software)
    except:
      continue
  if not softwares:
    raise Http404
  return render(request,'softwares/linux.html',{
      'check':check,
      'softwares':softwares,})

def software_search(request):
  if request.is_ajax():
    s = request.GET.get('term','')
    softwares = Software.objects.filter(Q(soft_name__icontains = s)|Q(version__icontains = s)|Q(description__icontains = s))[:5]
    def software_dict(software):
      return {
        'id':software.pk,
        'label':str(software),
        'value':str(software.soft_name)
      }
    data = json.dumps(map(software_dict,softwares))
  else:
    data = 'Fail'
  return HttpResponse(data, 'application/json ')
