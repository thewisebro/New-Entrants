from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from xhtml2pdf import pisa
from sets import Set
from gate.models import Gate
from gate.forms import *
from gate.constants import *
from nucleus.models import Faculty

import csv
import logging, datetime
import cStringIO as StringIO
from django.conf import settings

@login_required

def index1(request):
  person = Faculty.objects.get(user = request.user)

  if Gate.objects.filter(prof = person).exists():
    fac = Gate.objects.filter(prof = person)[0]
  else:
    fac = Gate.objects.create(prof = person)

  if request.method == 'GET':
    if fac.saved==True:
      return render_to_response('gate/gate_success.html',context_instance = RequestContext(request))
    else:
      form = DeclarationForm()
      return render_to_response('gate/index2.html',{'form' : form},context_instance = RequestContext(request))
  else:
   form1 = DeclarationForm(request.POST)
   if form1.is_valid():
     form1.process()
     if form1.cleaned_data['accept_1'] and form1.cleaned_data['accept_2'] and form1.cleaned_data['accept_3'] and form1.cleaned_data['accept_4'] and form1.cleaned_data['accept_5']:
       fac.declaration = True
       fac.save()
       return HttpResponseRedirect('/gate/gate/')
     else:
      return render_to_response('gate/index2.html',{'form' : form1},context_instance = RequestContext(request))
   else:
     return render_to_response('gate/index2.html',{'form' : form1},context_instance = RequestContext(request))

@login_required
def index(request):
#messages.success(request,'hellovb')
  err = 0
  person = Faculty.objects.get(user = request.user)
  print person.user.name
  print person.user.birth_date
  if Gate.objects.filter(prof = person).exists():
    fac = Gate.objects.filter(prof = person)[0]
  else:
    fac = Gate.objects.create(prof = person)

  if request.method == 'POST':
    form = GateForm(request.POST)
#  import ipdb;ipdb.set_trace()
    if form.is_valid():
      form.process()
      fac.prof=person
      fac.grade_pay = form.cleaned_data['grade_pay']
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
      fac.mobile_no = form.cleaned_data['mobile_no']
      cities_list = []
      cities_set = []
      cities_none = 0
      fac.city_pref1 = form.cleaned_data['city1']
      if fac.city_pref1 == "None" or fac.city_pref1 == "Any Of These" :
        cities_none = cities_none + 1
      else:
        cities_list.append(fac.city_pref1)
      fac.city_pref2 = form.cleaned_data['city2']
      if fac.city_pref2 == "None" or fac.city_pref2 == "Any Of These" :
        cities_none = cities_none + 1
      else:
        cities_list.append(fac.city_pref2)
      fac.city_pref3 = form.cleaned_data['city3']
      if fac.city_pref3 == "None" or fac.city_pref3 == "Any Of These" :
        cities_none = cities_none + 1
      else:
        cities_list.append(fac.city_pref3)
      fac.city_pref4 = form.cleaned_data['city4']
      if fac.city_pref4 == "None" or fac.city_pref4 == "Any Of These" :
        cities_none = cities_none + 1
      else:
        cities_list.append(fac.city_pref4)
      fac.city_pref5 = form.cleaned_data['city5']
      if fac.city_pref5 == "None" or fac.city_pref5 == "Any Of These" :
        cities_none = cities_none + 1
      else:
        cities_list.append(fac.city_pref5)
      fac.city_pref6 = form.cleaned_data['city6']
      if fac.city_pref6 == "None" or fac.city_pref6 == "Any Of These" :
        cities_none = cities_none + 1
      else:
        cities_list.append(fac.city_pref6)

      cities_set = Set(cities_list)
      print len(cities_set)+cities_none
      if len(cities_set)+cities_none == 6:

        fac.saved = True
        fac.save()
        person.user.contact_no = form.cleaned_data['phone_no_office']
        person.user.email = form.cleaned_data['email']
        person.user.birth_date = form.cleaned_data['date_of_birth']
        person.address = form.cleaned_data['home_address']
        person.date_of_joining = form.cleaned_data['date_of_join']
        person.department = form.cleaned_data['department']
        person.designation = form.cleaned_data['designation']
        person.employee_code = form.cleaned_data['employee_id']
        person.save()
        messages.success(request,"Success")
        return render_to_response('gate/gate_success.html',context_instance = RequestContext(request))
      else:
        err = 1
        print err
        return render_to_response('gate/index1.html',{'form' : form,'err':err},context_instance = RequestContext(request))
    else:
      print 'hello'
      return render_to_response('gate/index1.html',{'form' : form},context_instance = RequestContext(request))
  else:
    print 'yoyo'
#    import ipdb;ipbd.set_trace()
    print person.user.birth_date
    if fac.saved==False:
      if fac.declaration==True:
        birth_date = person.user.birth_date
        join_date = person.date_of_joining
        curr_date = datetime.datetime.now().date()
        curr_date = curr_date.strftime('%d-%m-%Y')
        age = 0
        try:
          if birth_date:
            delta = curr_date - birth_date
            age = delta.days/365
            birth_date = birth_date.strftime('%d-%m-%Y')
        except:
          pass
        try:
          if join_date:
            join_date = datetime.datetime.strptime(join_date,'%Y-%m-%d').date()
            join_date = join_date.strftime('%d-%m-%Y')
        except:
          pass
        form = GateForm(initial = {
            'name': person.user.name,
            'employee_id': person.employee_code,
            'designation': person.designation,
            'department': person.department,
            'date_of_join': join_date,
            'date_of_birth':birth_date,
            'home_address': person.address,
            'phone_no_office': person.user.contact_no,
            'email': person.user.username+'@iitr.ac.in',
            'age':age,
            })
        return render_to_response('gate/index1.html',{'form' : form,'curr_date':curr_date},context_instance = RequestContext(request))
      else:
        return HttpResponseRedirect('/gate/gate1')
    else:
      return render_to_response('gate/gate_success.html',context_instance = RequestContext(request))

@login_required
def gate_print_pdf(request):
  person = Faculty.objects.get(user = request.user)
  gate = Gate.objects.filter(prof = person)[0]
  title=""
  flag=0
  title="Details for GATE-JAM 2016"
  template_name = 'gate/gate_pdf.html'
  html = render_to_string(template_name, {
            'person' : person,
            'designation' : person.designation,
            'department' : person.department,
            'title':title,
            'date': datetime.datetime.now(),
            'mobile': gate.mobile_no,
            'email' : person.user.username+'@iitr.ac.in',
            'week_pref1': gate.week_pref1,
            'week_pref2': gate.week_pref2,
            'city_pref1': gate.city_pref1,
            'city_pref2': gate.city_pref2,
            'city_pref3': gate.city_pref3,
            'city_pref4': gate.city_pref4,
            'city_pref5': gate.city_pref5,
            'city_pref6': gate.city_pref6,
            },
            context_instance = RequestContext(request))
  result = StringIO.StringIO()
#  import pdb; pdb.set_trace()
  def fetch_resources(uri, rel):
    return os.path.join(settings.PROJECT_ROOT, 'static',
      uri.replace(settings.STATIC_URL, ''))
  pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('utf8')), result)
  result = result.getvalue()
  response = HttpResponse(result, content_type='application/pdf')
  response['Content-Disposition'] = ('attachment; filename=GATE_' + person.user.username
            + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") +'.pdf')
  response['Content-Length'] = len(result)
  return response

@login_required
@user_passes_test(lambda u: u.groups.filter(name = 'Gate Admin').exists())
def gate_allinfo(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="info.csv"'
  a = csv.writer(response)
  data = ['Name','Designation','Department','Employee_ID','Date_Of_JoiningIITR','Date Of Joining The Present Position','Mobile','Email','Week_1','Week_2','City_1','City_2','City_3','City_4','City_5','City_6']
  a.writerow(data)
  g = Gate.objects.all()
# import ipdb;ipdb.set_trace()
  for i in range(0,len(g)):
    print g[i].prof.user.name,i
    if g[i].saved==True:
      data = []
      data.append(g[i].prof.user.name)
      data.append(g[i].prof.designation)
      data.append(g[i].prof.department)
      data.append(g[i].prof.employee_code)
      data.append(g[i].prof.date_of_joining)
      data.append(g[i].date_of_join_position)
      data.append(g[i].mobile_no)
      data.append(g[i].prof.user.username+'@iitr.ac.in')
      data.append(g[i].week_pref1)
      data.append(g[i].week_pref2)
      data.append(g[i].city_pref1)
      data.append(g[i].city_pref2)
      data.append(g[i].city_pref3)
      data.append(g[i].city_pref4)
      data.append(g[i].city_pref5)
      data.append(g[i].city_pref6)
      a.writerow(data)
  return response

