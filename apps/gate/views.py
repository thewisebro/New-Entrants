from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from xhtml2pdf import pisa

from gate.models import Gate
from gate.forms import GateForm
from gate.constants import *
from nucleus.models import Faculty

import logging, datetime
import cStringIO as StringIO
from django.conf import settings

@login_required
def index(request):
#messages.success(request,'hellovb')
  person = Faculty.objects.get(user = request.user)
  print person.user.name
  print person.user.birth_date
  if Gate.objects.filter(prof = person).exists():
    fac = Gate.objects.filter(prof = person)[0]
  else:
    fac = Gate.objects.create(prof = person)

  if request.method == 'POST':
    form = GateForm(request.POST)
    string = ''
    if form.is_valid():
      form.process()
      fac.prof=person
      fac.grade_pay = form.cleaned_data['grade_pay']
      fac.acc_no = form.cleaned_data['account_no']
      fac.phone_office = form.cleaned_data['phone_no_office']
      fac.phone_resi = form.cleaned_data['phone_no_resi']
      fac.annual_income = form.cleaned_data['income']
      fac.height = form.cleaned_data['height']
      fac.weight = form.cleaned_data['weight']
      print 'here'
      fac.age=form.cleaned_data['age']
      fac.nominee_name=form.cleaned_data['nominee']
      fac.relation_nominee = form.cleaned_data['nominee_relation']
      fac.date_of_join_position = form.cleaned_data['date_of_joinPos']
      fac.week_pref1 = form.cleaned_data['pref1']
      fac.week_pref2 = form.cleaned_data['pref2']
      fac.city_pref1 = form.cleaned_data['city1']
      fac.city_pref2 = form.cleaned_data['city2']
      fac.city_pref3 = form.cleaned_data['city3']
      fac.city_pref4 = form.cleaned_data['city4']
      fac.city_pref5 = form.cleaned_data['city5']
      fac.city_pref6 = form.cleaned_data['city6']
      fac.save()
      person.user.contact_no = form.cleaned_data['mobile_no']
      person.user.email = form.cleaned_data['email']
      person.user.birth_date = form.cleaned_data['date_of_birth']
      person.address = form.cleaned_data['home_address']
      person.date_of_joining = form.cleaned_data['date_of_join']
      person.department = form.cleaned_data['department']
      person.designation = form.cleaned_data['designation']
      person.employee_code = form.cleaned_data['employee_id']
      person.save()
      messages.success(request,"Success")
      return HttpResponseRedirect(reverse('gate.views.index'))
  else:
    print 'yoyo'
#    import ipdb;ipbd.set_trace()
    print person.user.birth_date
    form = GateForm(initial = {
        'name': person.user.name,
        'employee_id': person.employee_code,
        'designation': person.designation,
        'department': person.department,
        'date_of_join': person.date_of_joining,
        'date_of_birth':person.user.birth_date,
        'home_address': person.address,
        'mobile_no': person.user.contact_no,
        'email': person.user.email,
        })
  return render_to_response('gate/index1.html',
      {'form' : form},
      context_instance = RequestContext(request))

