from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from application_form.models import *
from nucleus.models import Student




@login_required
def app_form(request):
  person = Student.objects.get(user=request.user)
  not_required_fields = StudentApplicationInfo.not_required_fields
  if person.semester.find('PHD') >= 0 or person.semester.find('PG') >= 0 :
    not_required_fields += ['jee_rank','jee_category_rank','category']

  if request.method == 'GET':
    form = StudentApplicationForm(person)
    if StudentApplicationInfo.objects.filter(user=request.user).exists():
      s = StudentApplicationInfo.objects.filter(user=request.user)[0]
      return render_to_response('application_form/form.html', {'form': form, 'prev':s, 'editable':StudentApplicationInfo.editable_fields, 'not_required':not_required_fields}, context_instance=RequestContext(request))
    else:
      return render_to_response('application_form/form.html', {'form': form,'editable':StudentApplicationInfo.editable_fields, 'not_required':not_required_fields}, context_instance=RequestContext(request))

  if request.method == 'POST':
    form = StudentApplicationForm(person, request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/app_form/')
    else:
      print 'invalid'
      return render_to_response('application_form/form.html', {'form': form , 'data':request.POST,'editable':StudentApplicationInfo.editable_fields, 'not_required':not_required_fields}, context_instance=RequestContext(request))

@login_required
def delete_form(request):
  s = StudentApplicationInfo.objects.filter(user=request.user) 
  if s.count() != 0:
    s = s[0]
    s.delete()
  return HttpResponseRedirect('/app_form/')
