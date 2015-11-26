from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.models import User

import simplejson as json
import xlwt
import datetime
from nucleus.models import Student, WebmailAccount
from placement import policy, forms
from placement.policy import current_session_year
from placement import utils
from placement.models import *
from placement.utils import *
from placement.forms import *
from placement.constants import *
from django.views.decorators.csrf import csrf_exempt

# XXX : Keep logged after all imports only
# As other imports might over write the logger
logger = logging.getLogger('placement')

l = logger

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def create_slot(request):
  slot_form = CreateSlotForm()
  message=''
  if request.method == "POST":
    try:
      slot_form = CreateSlotForm(request.POST)
      slot = CompanySlot()
      if slot_form.data.has_key('visibility'):
        slot.visibility = True
      else:
        slot.visibility = False
      slot.start_date = slot_form.data['start_date']
      slot.end_date = slot_form.data['end_date']
      slot.save()
      try:
        companies = slot_form.data['company'].split(",")
        for company in companies:
          obj = Company.objects.get(pk=int(company))
          slot.company.add(obj)
        slot.save()
        messages.success(request, "Slot created successfully")
      except:
        messages.error(request, "Please select company from autocomplete option.")
        slot.delete()
    except Exception as e:
      messages.error(request, "Some error occured. Please try again")
  slot_form = CreateSlotForm()
  existing_slots = CompanySlot.objects.all()
  dates = list(set([slot.start_date.date() for slot in existing_slots]))
  return render_to_response('placement/create_slots.html', {
      'slot_form': slot_form,
      'slots': existing_slots,
      'dates': dates,
#   'error_msg':message,
      },context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def delete_slot(request, slot_id):
  try:
    slot = CompanySlot.objects.get(id=slot_id)
    slot.delete()
    messages.success(request, "Slot deleted successfully.")
  except CompanySlot.DoesNotExist:
    messages.error(request, "Slot does not exist.")
  return HttpResponseRedirect(reverse('placement.views_slots.create_slot'))



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def company_search(request):
  return HttpResponse(utils.company_search(request),'application/json')

@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def edit_slot(request, slot_id):
  message = ''
  if slot_id:
    try:
      slot = CompanySlot.objects.get(pk=slot_id)
    except CompanySlot.DoesNotExist:
      raise Http404
  companies = slot.company.all()
  data = ""
  data_id = ""
  data_dict = {}
  for company in companies:
      if data == "":
        data +=str(company.name)
        data_id = str(company.id)
      else:
        data = data+","+str(company.name)
        data_id = data_id+","+str(company.id)
      data_dict[str(company.name)] = str(company.id)
  slot_data = {'visibility': slot.visibility,
               'start_date': slot.start_date.strftime("%Y-%m-%d %H:%M"),
               'end_date': slot.end_date.strftime("%Y-%m-%d %H:%M"),
               'status': slot.status,
               'company': data}
  edit_form = EditSlotForm(initial=slot_data)

  if request.method == "POST":
    try:
      edit_form = EditSlotForm(request.POST)
      slot = CompanySlot.objects.get(pk=slot_id)
      slot.start_date = str(edit_form.data['start_date'])
      slot.end_date = str(edit_form.data['end_date'])
      if edit_form.data.has_key('visibility'):
        slot.visibility = True
      else:
        slot.visibility = False
      if edit_form.data.has_key('status'):
        slot.status = True
      else:
        slot.status = False
      companies = edit_form.data['company'].split(",")
      for x in slot.company.all():
        slot.company.remove(x)
      for company in companies:
        obj = Company.objects.get(pk=int(company))
        slot.company.add(obj)
      slot.save()
      messages.success(request, "Slot updated successfully")
      return HttpResponseRedirect(reverse('placement.views_slots.create_slot'))
    except Exception as e:
      messages.error(request, "Some error occured. Please try again")

  return render_to_response('placement/edit_slots.html',{
       'form': edit_form,
       'data_id':data_id,
       'data_dict':data_dict,
#       'error_msg':message
       'slot': slot},context_instance=RequestContext(request))

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
@user_passes_test(lambda u: u.username in SLOTS_TESTING_PERMISSION, login_url=login_url)
def view_slot(request, slot_id):

  user = request.user
  student = user.student
  placement_person = PlacementPerson.objects.get_or_create(student=student)[0]
  if not placement_person.status=='VRF':
    messages.error("Your Placement status is not verified. If you are in final year, please contact Placement office immediately.")
    return render_to_response('placement/slots.html',{
      'message': message
      }, context_instance=RequestContext(request))
  message=""
  company_maps = CompanyApplicationMap.objects.filter(plac_person=placement_person, shortlisted=True)
  company_eligible = [l.company for l in company_maps]

  company_data = []
  try:
    slot = CompanySlot.objects.get(visibility=True, pk=slot_id)
    companies = slot.company.all()
    company_info = []
    for company in companies:
      data = company.ctc_remark
      if not company.ctc_remark:
        data = "-"
      l = {'Name': company.name,
           'CTC': data}
      company_info.append(l)

    company_eligible_list = []
    for company in slot.company.all():
      if company in company_eligible:
        company_eligible_list.append(company)

    for company in company_eligible_list:
      created_list = []
      priority_data, created = CompanyPlacementPriority.objects.get_or_create(student=student, slots=slot, company=company)
      if not created :
        created_list.append(False)
      company_data.append(priority_data)
    priority_id = [l.priority for l in company_data]
    new_priority_list = [x for (y,x) in sorted(zip(priority_id, company_data))]
    company_data = new_priority_list
  except CompanySlot.DoesNotExist:
    raise Http404
  if request.method == "POST":
    if slot.status == False:
      message = "This incident has been reported. In case of any discrepancy, please contact Placement office."
      is_success = False
      json_data = json.dumps({'message': message, 'is_success': is_success})
      return HttpResponse(json_data, content_type='application/json')
    data = json.loads(request.POST.items()[0][0])
    message = ""
    is_success = True

    for priority in data:
      try:
          company = Company.objects.get(pk=priority["id"])
          company_priority = CompanyPlacementPriority.objects.get_or_create(student=student, company=company, slots=slot)[0]
          company_priority.priority = int(priority["priority"])+1
          company_priority.save()
      except Exception as e:
        message = "Some error occured. Please contact IMG"
        is_success = False

    if not message:
      message = "Saved Successfully"
    json_data = json.dumps({'message': message, 'is_success': is_success})
    return HttpResponse(json_data, content_type='application/json')
  no_data_msg = ""
  if not company_data:
    no_data_msg = "You are not required to fill preferences for this slot. In case of any discrepancy, please contact Placement office immediately. "
  return render_to_response('placement/slots.html',{
      'data': company_data,
      'info': company_info,
      'messages': message,
      'slot':slot,
      'no_data_msg':no_data_msg,
      }, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
@user_passes_test(lambda u: u.username in SLOTS_TESTING_PERMISSION, login_url=login_url)
def view_all_slots(request):
  student = request.user.student
  plac_person = PlacementPerson.objects.get(student=student)
  message = ''
  if not plac_person.status=='VRF':
    message = "Your status is not verified. If you are in final year, please contact Placement office immediately."
    return render_to_response('placement/all_slots.html',{
        "message": message
        }, context_instance = RequestContext(request))
  try:
    slots = CompanySlot.objects.filter(visibility=True)
  except ObjectDoesNotExist:
    message = "There are no open slots."
  if not slots:
    message = "There are no open slots."
  return render_to_response('placement/all_slots.html',{
      'slots': slots,
      'message':message,
      }, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def export_slot_data(request, slot_id):
  company_priority = CompanyPlacementPriority.objects.filter(slots__id=slot_id)
  student_list = [l.student for l in company_priority]
  student_list = list(set(student_list))

  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('sheet 1')

  headers = ['Enrollment No', ' Name', 'CGPA', 'Email']
  slot = CompanySlot.objects.get(pk=slot_id)
  companies_count = slot.company.all().count()
  companies = slot.company.all()
  for count in range(companies_count):
      headers.append("Priority "+str(count+1))
  new_lst = []
  for people in student_list:
    try:
      priority = CompanyPlacementPriority.objects.filter(slots__id=slot_id,student=people).order_by('priority')
      company_pri = [x.company.name for x in priority]
      while len(company_pri) < companies_count:
        company_pri.append('-')
      a = [people.user.username, people.user.name, people.cgpa, people.user.email]
      a.extend(company_pri)
      new_lst.append(a)
    except Exception as e:
      print str(e)
      message = "Some error occured while generating xls"
  try:
    lst_len = len(new_lst[0])
  except IndexError:
    lst_len = 0
  print new_lst
  for (col, heading) in enumerate(headers):
     ws.write(2, col+1, heading)
  row = 3
  for data in new_lst:
   for r in range(len(data)):
     ws.write(row, r+1, data[r])
   row +=1

  file_name = str(str(slot.start_date)+'--'+str(slot.end_date))
  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename=%s.xls'%file_name
  wb.save(response)
  return response

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def export_final_slot_result(request, slot_id):

  if request.method == "POST":
    company_priority = CompanyPlacementPriority.objects.filter(slots__id=slot_id)
    students = []
    for priority in company_priority:
      students.append(priority.student)
    students = [l for l in students if not l]
    selected_applications = []
    for priority in company_priority:
      application = CompanyApplicationMap.objects.filter(company=priority.company, student=priority.student, status='SEL')
      selected_applications.append(aplication)
      pass
