from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

import logging

from django.contrib import messages

from placement.forms import BaseModelFormFunction
from placement import forms
from placement.policy import current_session_year
from placement.models import *
from placement.utils import *

import shutil
import json

l = logging.getLogger('placement')

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# IMPORTANT : Objects of Student and PlacementPerson are to be stored in session.
# These objects are used in all the templates.

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
#@user_passes_test(lambda u: WorkshopRegistration.objects.filter(placement_person__student__user = u).exists() or u.student.placementperson.status != 'VRF', login_url='/placement/workshop_registration')
def list(request) :
  """
  Displays the list of companies to student. The student can apply to a company if that company
  is open for his discipline. He has a withdraw option if he has already applied to a company.
  The current status of the application to a company is also shown.
  """
  try :
    l.info(request.user.username + ': viewed list of companies.')
    companies = Company.objects.filter(year = current_session_year() )
    student = request.user.student
    plac_person = student.placementperson
    status = [] # list to store the status of the application in order of the list "companies"
    # Different status possible are
    #   1. NOT - Not applicable
    #   2. NAP - Not Applied
    #       + other status from placement.constants.COMPANY_APPLICATION_STATUS

    opencompanies = []
    avlstatus = [] #status of companies which are availabe for application by the student
    for company in companies :
      try :
        application = CompanyApplicationMap.objects.get(company = company, plac_person = plac_person)
        status.append(application.status)
      except CompanyApplicationMap.DoesNotExist as e:
        status.append('NAP')

      if company.status == 'OPN' and student.branch in company.open_for_disciplines.all():
        opencompanies.append(company)
        try:
          application = CompanyApplicationMap.objects.get(company = company, plac_person = plac_person)
          avlstatus.append(application.status)
        except:
          avlstatus.append('NAP')
    company_status_map = zip(companies, status)
    avl_company_status_map = zip(opencompanies, avlstatus)
    return render_to_response('placement/company_list.html', {
        'company_status_map' : company_status_map,
        'avl_company_status_map' : avl_company_status_map,
        'student' : student,
        'plac_person' : plac_person
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': encountered error in viewing company list')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def info(request, company_id) :
  try :
    l.info(request.user.username + ': viewed company info for ' + company_id)
    #year = current_session_year()
    company = get_object_or_404(Company, pk = company_id)
    form = BaseModelFormFunction(Company, exclude_list = ('open_for_disciplines', 'year'), instance = company)
    return render_to_response('placement/generic_locked.html', {
        'form' : form,
        'title' : company.name
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': encountered error in viewing company ' + company_id)
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
#@user_passes_test(lambda u: WorkshopRegistration.objects.filter(placement_person__student__user = u).exists() or u.student.placementperson.status != 'VRF', login_url='/placement/workshop_registration')
def open_to(request, company_id) :
  """
  Displays the name of branches for which a company is open.
  """
#  try :
  l.info(request.user.username + ': viewing company open to for ' + company_id)
  company = get_object_or_404(Company, id = company_id, year = current_session_year())
  opento = company.open_for_disciplines.all().order_by('graduation', 'name')
  return render_to_response('placement/company_opento.html', {
      'company' : company,
      'opento' : opento
      }, context_instance = RequestContext(request))
#  except Exception as e :
#    l.info(request.user.username + ': encountered error in viewing company.open to for ' + company_id)
#    l.exception(e)
#    return handle_exc(e, request)

# Placement Admin views start
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def add(request) :
  try :
    l.info (request.user.username + ': Trying to add a company')
    if request.method == 'POST' :
      form = forms.CompanyForm(request.POST, request.FILES)
      if form.is_valid() :
        instance = form.save(commit = False)
        instance.year = current_session_year()
        instance.save()
        form.save_m2m()
        l.info (request.user.username + ': Successfully added company ' + str(instance.id))
        messages.success(request, 'Successfully created the company.')
        return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
    else :
      form = forms.CompanyForm()
    # Remove the default help text for a ManyToManyFeild
    form.fields['open_for_disciplines'].help_text = None
    return render_to_response('placement/basic_form.html', {
        'form' : form,
        'title' : 'New Company',
        'name' : 'company_addition',
        'action' : reverse('placement.views_company.add'),
        'branches_button_required' : True,
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': encountered error in addding a company')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def admin_list(request) :
  """
    Show list of companies to admin for editing
  """
  try :
    l.info(request.user.username + ': viewing company list(admin)')
    year = current_session_year()
    companies = Company.objects.filter(year = year)
    return render_to_response('placement/company_list_admin.html', {
        'companies' : companies
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': encountered error in viewing company list')
    l.exception(e)
    return handle_exc(e, request)

# TODO : Take care of the second round stuff.

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def edit(request, company_id) :
  """
    Edit a company
  """
  try :
    l.info(request.user.username + ': trying to edit a company.')
    year = current_session_year()
    company = get_object_or_404(Company, pk = company_id, year = year)
    if request.method == 'POST' :
      form = forms.CompanyForm(request.POST, request.FILES, instance = company)
      if form.is_valid() :
        form.save()
        l.info(request.user.username + ': Edited company successfully ' + company_id)
        messages.success(request, 'Updated the company.')
        return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
    else :
      form = forms.CompanyForm(instance = company)
      if company.brochure :
        # Change the url of brochure
        company.brochure.name = u'placement/brochures/' + unicode(company.id) + '/'
    # Remove the default help text for a ManyToManyFeild
    form.fields['open_for_disciplines'].help_text = None
    return render_to_response('placement/basic_form.html', {
        'form' : form,
        'title' : company.name,
        'action' : reverse('placement.views_company.edit', args=[company_id]),
        'branches_button_required' : True,
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': encountered error in editing a company')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def delete(request, company_id) :
  """
    Deleting a company
  """
  try :
    l.info(request.user.username + ': Deleting company ' + company_id)
    year = current_session_year()
    company = get_object_or_404(Company, pk = company_id, year = year)
    company.delete()
    filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications', 'company'+company_id)
    if os.path.exists(filepath):
      shutil.rmtree(filepath)
    l.info(request.user.username + ': Successfully deleted company ' + company_id)
    messages.success(request, 'The company was deleted successfully.')
    return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
  except Exception as e:
    l.info(request.user.username + ': encountered error in deleting a company')
    l.exception(e)
    return handle_exc(e, request)


def is_eligible_for_workshop(student):
  if student.branch.degree in ['B.Tech.', 'B.Arch.', 'IDD', 'IMT', 'IMSc']:
    duration = student.branch.duration/2
    if not student.branch.duration%2 == 0:
      duration = (student.branch.duration+1)/2
    if duration == int(student.semester[-2]):
      return True
    else:
      return False
  else:
    return False

#@csrf_exempt
#@login_required
#def set_workshop_priority(request):
#  student = request.user.student
#  if not is_eligible_for_workshop(student):
#    access_message = "Workshop registration is not open for your branch. In case of any discrepancy, please contact IMG."
#    return render_to_response('placement/workshop_priority.html', {
#      "access_message": access_message,
#        }, context_instance = RequestContext(request))
#  workshop_days = [ '2nd September 06:00pm-10:00pm, Tuesday',
#                    '3rd September 06:00pm-10:00pm, Wednesday',
#                    '4th September 06:00pm-10:00pm, Thursday',
#                    '5th September 06:00pm-10:00pm, Friday',
#                    '6th September 11:30am-03:30pm, Saturday']
#  priority, created = WorkshopPriority.objects.get_or_create(student=student)
#  is_checked = False
#  if not created:
#    priority_list = [int(priority.day1_priority),int(priority.day2_priority),int(priority.day3_priority),int(priority.day4_priority),int(priority.day5_priority)]
#    workshop_days = [x for (y,x) in sorted(zip(priority_list,workshop_days))]
#    is_checked = priority.interview_application
#  message=""
#  if request.method == "POST":
#    try:
#      priority = WorkshopPriority.objects.get(student=student).delete()
#      priority = WorkshopPriority.objects.create(student=student)
#      data = json.loads(request.POST.items()[0][0])
#      is_success="True"
#      for l in data:
#         if l.has_key('id'):
#           if l['id']=='2nd September 06:00pm-10:00pm, Tuesday':
#             priority.day1_priority = int(l['priority'])+1
#           elif l['id']=='3rd September 06:00pm-10:00pm, Wednesday':
#             priority.day2_priority = int(l['priority'])+1
#           elif l['id']=='4th September 06:00pm-10:00pm, Thursday':
#             priority.day3_priority = int(l['priority'])+1
#           elif l['id']=='5th September 06:00pm-10:00pm, Friday':
#             priority.day4_priority = int(l['priority'])+1
#           elif l['id']=='6th September 11:30am-03:30pm, Saturday':
#             priority.day5_priority = int(l['priority'])+1
#         elif l.has_key('apply'):
#            priority.interview_application = l["apply"]
#
#      priority.save()
#      message = "Saved Successfully"
#    except Exception as e:
#      message = "Some error occured. Please contact IMG"
#      is_success = False
#    json_data = json.dumps({'message':message, 'is_success':is_success})
#    return HttpResponse(json_data, mimetype='application/json')
#
#  return render_to_response('placement/workshop_priority.html', {
#      "data": workshop_days,
#      "is_checked": is_checked,
#      "message": message,
#        }, context_instance = RequestContext(request))
#
#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
#def workshop_registration(request):
#  student = request.user.student
#  plac_person = student.placementperson
#  if plac_person.status not in ['VRF', 'OPN', 'LCK']:
#    messages.error(request, 'You can not register for workshop. In case of any disperency, please contact IMG.')
#    return HttpResponseRedirect(reverse('placement.views.index'))
#  prev_registration = WorkshopRegistration.objects.get_or_none(placement_person = plac_person)
#  registration_form = forms.WorkshopRegistrationForm(instance = prev_registration)
#  if request.method=="POST":
#    registration_form = forms.WorkshopRegistrationForm(request.POST, instance = prev_registration)
#    if registration_form.is_valid():
#      registration_obj = registration_form.save(commit=False)
#      registration_obj.placement_person = plac_person
#      l.info(request.user.username + ': workshop registration status changed to '+str(registration_obj.is_registered))
#      if registration_obj.is_registered:
#        registration_obj.save()
#        messages.success(request, 'Successfully registered for Workshop.')
#      else:
#        registration_obj.delete()
#        messages.success(request, 'Successfully de-registered for Workshop.')
#      return HttpResponseRedirect(reverse('placement.views_company.workshop_registration'))
#    else:
#      l.info(request.user.username + ': Error saving workshop registration detail')
#      messages.error(request, 'Unknown error occured.')
#      return HttpResponseRedirect(reverse('placement.views_company.workshop_registration'))
#
#  return render_to_response('placement/basic_form.html',{
#      "title": "Workshop Registration 4P Education",
#      "action": "",
#      "name": "workshop_registration",
#      "form": registration_form,
#      "editable_warning": "",
#      }, context_instance = RequestContext(request))
#

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def workshop_registration(request):
  student = request.user.student
  plac_person = student.placementperson
  if plac_person.status != 'VRF':
    messages.error(request, 'You can not register for workshop. Only verified students can register for workshop.')
    return HttpResponseRedirect(reverse('placement.views.index'))
  prev_registration = WorkshopRegistration.objects.get_or_none(placement_person = plac_person)
  registration_form = forms.WorkshopRegistrationForm(instance = prev_registration)
  if request.method=="POST":
    registration_form = forms.WorkshopRegistrationForm(request.POST, instance = prev_registration)
    try:
      if registration_form.is_valid():
        registration_obj = registration_form.save(commit=False)
        if registration_obj.options not in ['NOT','4P Education','Ethuns Consultancy Service']:
          registration_obj.reason = ""
        registration_obj.placement_person = plac_person
        registration_obj.save()
        l.info(request.user.username + ': workshop registration successful')
        messages.success(request, 'Successfully registered for Workshop.')
        return HttpResponseRedirect(reverse('placement.views_company.workshop_registration'))
      else:
        l.info(request.user.username + ': Error saving workshop registration detail')
        messages.error(request, 'Unknown error occured.')
        return HttpResponseRedirect(reverse('placement.views_company.workshop_registration'))
    except ValidationError as e:
      l.error(request.user.username + ': Error saving workshop registration detail')
      messages.error(request, str(e[0]))
      return HttpResponseRedirect(reverse('placement.views_company.workshop_registration'))
  if not WorkshopRegistration.objects.filter(placement_person=plac_person).exists():
    messages.error(request, 'Please fill workshop registration details. Deadline is 14th September.')
  return render_to_response('placement/workshop_registration.html',{
      "title": "Workshop Registration",
      "action": "",
      "workshop_registration_jquery": True,
      "name": "workshop_registration",
      "form": registration_form,
      "editable_warning": "",
      }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Student').exists(), login_url=login_url)
def workshop_registration_details(request):
  term = request.GET.get('q')
  return render_to_response('placement/workshop_details.html', {
      "term": term,
      }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def workshop_registration_export(request):
  import xlwt
  l.info(request.user.username + ': Exported Workshop Registration File')
  registered_lst = WorkshopRegistration.objects.all().order_by('options','placement_person__student__user__username')
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Sheet 1')

  ws.write(0, 0, 'Sr. No.')
  ws.write(0, 1, 'Enrollment No.')
  ws.write(0, 2, 'Name')
  ws.write(0, 3, 'Selected Option')
  ws.write(0, 4, 'Reason')

  lst = registered_lst.values_list('placement_person__student__user__username', 'placement_person__student__user__name', 'options', 'reason')
  for row, rowdata in enumerate(lst):
    ws.write(row+1, 0, row+1)
    for col, val in enumerate(rowdata):
      ws.write(row+1, col+1, val)

  response = HttpResponse(content_type='application/vnd.ms-excel')
  response['Content-Disposition']='attachment; filename=workshop_data.xls'
  wb.save(response)
  return response

