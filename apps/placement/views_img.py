from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import json as simplejson
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
import logging, os
import xlrd
import xlwt
import datetime
from nucleus.models import Student, WebmailAccount, User, Group
from placement import policy, forms
from placement.policy import current_session_year
from placement.models import *
from placement.forms import *
from placement.utils import *
from django.views.generic import FormView

# XXX : Keep logged after all imports only
# As other imports might over write the logger
logger = logging.getLogger('placement')

l = logger

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Admin').exists(), login_url=login_url)
def update_status(request):
  """
    Change placement status of a student. Only available to IMG members.
  """
  l.info(request.user.username+': opened view to change/check status, which open only to IMG members')
  plac_person = None
  old_status = None
  if request.method == 'POST' :
    check_status_form=CheckStatus(request.POST)
    form = ChangeStatus(request.POST)
    if form.is_valid() :
      check_status_form= CheckStatus()
      username = form.cleaned_data['enrollment_no']
      status = form.cleaned_data['status']
      try:
        try:
          plac_person = PlacementPerson.objects.get(student__user__username = username)
        except PlacementPerson.DoesNotExist as e :
          webmail = WebmailAccount.objects.get(webmail_id = username)
          plac_person = PlacementPerson.objects.get(student__user = webmail.user)
        old_status = plac_person.status
        plac_person.status = status
        plac_person.save()
        l.info(request.user.username+': changed status of ' + plac_person.student.user.username + ' ('+plac_person.student.name+') from '+ old_status +' to '+plac_person.status)
        messages.success(request, 'Status of '+plac_person.student.name+'('+username+') changed from '+ old_status +' to '+plac_person.status)
      except Exception as e:
          logger.info(request.user.username+': got an exception in changing status of '+username)
          logger.exception(e)
          messages.error(request, 'Placement Student does not exist with enrollment no '+username)
    if check_status_form.is_valid():
      username=check_status_form.cleaned_data['enrollment_no']
      try:
        plac_person = PlacementPerson.objects.get(student__user__username = username)
      except PlacementPerson.DoesNotExist as e :
        webmail = WebmailAccount.objects.get(webmail_id = username)
        plac_person = PlacementPerson.objects.get(student__user = webmail.user)
      l.info(request.user.username+': viewed status of ' + plac_person.student.user.username + ' ('+plac_person.student.name+')')
      old_status= plac_person.status
      form = ChangeStatus()
  else :
    form = ChangeStatus()
    check_status_form=CheckStatus()
  return render_to_response('placement/change_status.html', {
      'form' : form,
      'check_status_form': check_status_form,
      'submit' : 'Submit',
      'old_status_for_checking' : old_status,
      'plac_person' : plac_person,
      },
      context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Admin').exists(), login_url=login_url)
def generate_registration_no(request):
  """
    Generate Registration no. of a student. Only available to IMG members.
  """
  l.info(request.user.username+': opened view to generate registration no, which open only to IMG members')
  if request.method == 'POST' :
    form = GenerateRegistrationNo(request.POST)
    if form.is_valid() :
      username = form.cleaned_data['enrollment_no']
      try:
        try:
          plac_person = PlacementPerson.objects.get(student__user__username = username)
        except PlacementPerson.DoesNotExist as e :
          webmail = WebmailAccount.objects.get(webmail_id = username)
          plac_person = PlacementPerson.objects.get(student__user = webmail.user)
        student = plac_person.student
        info = PlacementInformation.objects.get_or_create(student = student)[0]
        info.registration_no  = student.branch.degree + '/' + student.branch.code + '/' + student.user.username + '/'
        year = current_session_year() + 1
        info.registration_no += str(year)
        info.save()
        l.info(request.user.username+': generated registration no of ' + plac_person.student.user.username + ' ('+plac_person.student.name+')')
        messages.success(request, 'Successfully generated registration no of '+plac_person.student.name+'('+username+'): '+info.registration_no)
      except Exception as e:
          logger.info(request.user.username+': got an exception in generating registration no of '+username)
          logger.exception(e)
          messages.error(request, 'Placement Student does not exist with enrollment no '+username)
    else:
      messages.error(request, form.errors, extra_tags='form_error')
  else :
    form = GenerateRegistrationNo()
  return render_to_response('placement/generate_registration_no.html', {
      'form' : form,
      'submit' : 'Submit',
      },
      context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='IMG Admin').exists(), login_url=login_url)
def generate_missing_resumes(request, company_id):
  """
    To generate missing resumes of a company. Only available for IMG members.
  """
  l.info(request.user.username+': Opened view to generate missing resumes')
  error_msg = None
  try:
    company = Company.objects.get(pk = company_id)
  except CompanyDoesNotExist as e:
    error_msg = 'Company Does Not Exist'
  applications = CompanyApplicationMap.objects.filter(company = company)
  errors = []
  filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications', 'company'+str(company_id), str(request.user.username)+'.pdf')
  parent = os.path.split(filepath)[0]
  if not os.path.exists(parent) :
    os.makedirs(parent)
  for a in applications :
    student = a.plac_person.student
    filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications', 'company'+str(company_id), str(student.user.username)+'.pdf')
    # Make sure that the parent directory of filepath exists
    try:
      with open(filepath) as f: pass
    except IOError as e:
      pdf = get_resume_binary(RequestContext(request), student, company.sector)
      if pdf['err'] :
        return HttpResponse('Your resume cannot be generated. Please contact IMG immediately.')
      resume = open(filepath, 'w')
      resume.write(pdf['content'])
      resume.close()
      errors.append(student)
  return render_to_response('placement/generate_missing_resumes.html', {
                            'error_msg' : error_msg,
                            'errors' : errors,
                            }, context_instance = RequestContext(request))


#@login_required
#@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager', 'Company Coordinator']).exists() , login_url=login_url)
#def contactmanager_edit(request, company_id=None):
#  if company_id:
#    try:
#      company = CompanyContact.objects.get(pk = company_id)
#    except ObjectDoesNotExist:
#      messages.error(request, 'The company has been deleted or removed')
#
#    companydata = {'company_name':company.company_name,
#      'status':company.status,
#      'comments':company.comments,
#      'cluster':company.cluster,
#      'last_contact':company.last_contact,
#      'person_in_contact':company.person_in_contact,
#      'when_to_contact':company.when_to_contact}
#
#    companyform = CompanycontactForm(initial = companydata)
#
#    contactperson = ContactPerson.objects.get(pk = company.contactperson_id)
#
#    contactpersondata = {'email':contactperson.email,
#      'contact_person':contactperson.contact_person,
#      'phone_no':contactperson.phone_no,
#      'designation':contactperson.designation}
#    contactpersonform = ContactpersonForm(initial = contactpersondata)
#    try:
#      companycoordi = CompanyCoordi.objects.get(student__user__name=company.person_in_contact)
#    except ObjectDoesNotExist:
#      companycoordi = None
#    company_coordidata = {'company_coordinator': companycoordi}
#    assignform = AssignCoordinatorForm(initial = company_coordidata)
#
#  else:
#    companyform = CompanycontactForm()
#    contactpersonform = ContactpersonForm()
#    company = CompanyContact()
#    contactperson = ContactPerson()
#    companycoordi = CompanyCoordi()
#    assignform = AssignCoordinatorForm()
#
#  if request.method == 'POST' :
#     companyform = CompanycontactForm(request.POST)
#     contactpersonform = ContactpersonForm(request.POST)
#     assignform = AssignCoordinatorForm(request.POST)
#
#     if companyform.is_valid() and contactpersonform.is_valid() and assignform.is_valid():
#
#       contactperson.contact_person=contactpersonform.cleaned_data['contact_person']
#       contactperson.phone_no=contactpersonform.cleaned_data['phone_no']
#       contactperson.email=contactpersonform.cleaned_data['email']
#       contactperson.designation=contactpersonform.cleaned_data['designation']
#       contactperson.save()
#
#       company, created = CompanyContact.objects.get_or_create(contactperson=contactperson)
#
#       company.company_name=companyform.cleaned_data['company_name']
#       company.cluster=companyform.cleaned_data['cluster']
#       company.status=companyform.cleaned_data['status']
#       company.comments=companyform.cleaned_data['comments']
#       if request.POST.get('changelastcontact'):
#         company.last_contact = datetime.date.today()
#       company.when_to_contact=companyform.cleaned_data['when_to_contact']
#       try:
#        if request.user.groups.filter(name="Company Coordinator"):
#          companycoordi = CompanyCoordi.objects.get(student__user__name=company.person_in_contact)
#        else:
#          companycoordi = CompanyCoordi.objects.get(student__user__name=assignform.cleaned_data['company_coordinator'])
#        company.person_in_contact = companycoordi.student.name
#       except ObjectDoesNotExist:
#        company.person_in_contact = None
#       company.save()
#       if not request.user.groups.filter(name="Placement Manager"):
#          return HttpResponseRedirect('/placement/company_coordinator/')
#       return HttpResponseRedirect('/placement/contact_manager/')
#
#  return render_to_response('placement/plcmgr_manual.html',{
#       'companyform': companyform,
#       'contactpersonform':contactpersonform,
#       'assignform': assignform,
#       },context_instance  =RequestContext(request))
#
#@login_required
#@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
#def assign_company_coordinator(request):
#  if request.method == 'POST':
#    company_id_list = request.POST.getlist('assigns')
#    company_coordinator = request.POST.get('company_coordinator')
#    company_coordinator = CompanyCoordi.objects.get(id=company_coordinator)
#    for company_id in company_id_list:
#        company = CompanyContact.objects.get(pk = company_id)
#        company.person_in_contact = company_coordinator.student.name
#        company.save()
#    return HttpResponseRedirect('/placement/contact_manager/')
#
#@login_required
#@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager', 'Company Coordinator']).exists() , login_url=login_url)
#def contactmanager_delete(request, company_id):
#  try:
#    company = CompanyContact.objects.get(pk = company_id)
#    company.delete()
#    contactperson = ContactPerson.objects.get(pk = company.contactperson_id)
#    contactperson.delete()
#  except ObjectDoesNotExist:
#    messages.error(request, 'The company contact has been already deleted')
#
#  if not request.user.groups.filter(name="Placement Manager"):
#    return HttpResponseRedirect('/placement/company_coordinator/')
#  return HttpResponseRedirect('/placement/contact_manager/')
#
#
#@login_required
#@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
#def generate_company_contact_xls(request):
#  if request.method == 'POST':
#    company = CompanyContact.objects.all()
#    wb = xlwt.Workbook(encoding='utf-8')
#    ws = wb.add_sheet('sheet 1')
#
#    ws.write(0, 0, 'Company Name' )
#    ws.write(0, 1, 'Cluster' )
#    ws.write(0, 2, 'Contact Student' )
#    ws.write(0, 3, 'Designation' )
#    ws.write(0, 4, 'Phone Number' )
#    ws.write(0, 5, 'Email' )
#    ws.write(0, 6, 'Status' )
#    ws.write(0, 7, 'Last Contact' )
#    ws.write(0, 8, 'Student in Contact' )
#    ws.write(0, 9, 'Comments')
#    ws.write(0, 10, 'When to contact')
#
#    lst = company.values_list('company_name', 'cluster',
#              'contactperson__contact_person', 'contactperson__designation', 'contactperson__phone_no',
#              'contactperson__email', 'status', 'last_contact', 'person_in_contact', 'comments',
#              'when_to_contact')
#
#    for row, rowdata in enumerate(lst):
#       for col, val in enumerate(rowdata):
#         ws.write(row+1, col, val)
#
#    response = HttpResponse(content_type='application/vnd.ms-excel')
#    response['Content-Disposition'] = 'attachment; filename=placement_data.xls'
#    wb.save(response)
#    return response
#


@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator', 'Placement Manager']).exists() , login_url=login_url)
def company_coordinator_view(request):
  user =  request.user
  if user.groups.filter(name='Company Coordinator'):
    student = user.student
    campus_contact = CampusContact.objects.filter(student = student)
  elif user.groups.filter(name='Placement Manager'):
    campus_contact = CampusContact.objects.all()
  lst = []
  for campus_contact_inst in campus_contact:
    contactPerson = campus_contact_inst.contact_person
    values=[]
    values.append(contactPerson.company_contact.name)
    values.append(contactPerson.company_contact.cluster)
    values.append(contactPerson.name)
    values.append(contactPerson.designation)
    values.append(contactPerson.phone_no)
    values.append(contactPerson.email)
    values.append(contactPerson.company_contact.status)
    values.append(campus_contact_inst.last_contact)
    values.append(campus_contact_inst.student.user.name)
    comment = CompanyContactComments.objects.filter(campus_contact = campus_contact_inst).order_by('date_created')
    if comment:
      comment=comment[0].comment
    else:
      comment=""
    values.append(comment)
    values.append(campus_contact_inst.when_to_contact)
    values.append(campus_contact_inst.id)
    values.append(campus_contact_inst.id)
    lst.append(values[:])

  data_to_send = []

  for item in lst:
      a = []
      for x in list(item):
         try:
            if isinstance(x , datetime.date):
               df = DateFormat(x)
               dl = df.format(get_format('DATE_FORMAT'))
               a.append(str(dl))
            else:
               a.append(str(x))
         except UnicodeEncodeError:
            a.append('')
      data_to_send.append(a)

  return render_to_response('placement/company_coordi.html',{
        'contactperson_data' : data_to_send,
        }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
def placement_manager_view(request):
  assign_form = AssignCoordinatorForm()
  if request.method == 'POST' :
    pass
#    form = ExcelForm(request.POST , request.FILES)
#    if form.is_valid():
#      excel_file= request.FILES['excel_file']
#      workbook = xlrd.open_workbook(file_contents=excel_file.read())
#      worksheet = workbook.sheet_by_index(0)
#      num_rows = worksheet.nrows - 1
#      num_cells = worksheet.ncols -1
#      curr_row = 0
#      companyname = ""
#      while curr_row < num_rows:
#         curr_row += 1
#         row = worksheet.row(curr_row)
#         contactperson    = ContactPerson()
#         company          = CompanyContactInfo()
#
#         try:
#
#           company.name     = row[0].value.encode('ascii', 'ignore')
#           company.status           = row[6].value.encode('ascii', 'ignore')
#           company.last_contact     = row[7].value.encode('ascii', 'ignore')
#           company.person_in_contact= row[8].value.encode('ascii', 'ignore')
#           company.comments         = row[9].value.encode('ascii', 'ignore')
#           try:
#              company.cluster = int(row[1].value)
#           except ValueError:
#              pass
#           contactperson.name = row[2].value.encode('ascii', 'ignore')
#           contactperson.designation    = row[3].value.encode('ascii', 'ignore')
#           try:
#              contactperson.phone_no       = unicode(int(row[4].value)).encode('ascii', 'ignore')
#           except ValueError:
#              contactperson.phone_no       = unicode(row[4].value).encode('ascii', 'ignore')
#           contactperson.email          = row[5].value.encode('ascii', 'ignore')
#
#         except IndexError:
#             pass
#         contactperson.save()
#         company.contactperson = contactperson
#         company.save()
#
  else:
    form=ExcelForm()
  campus_contact = CampusContact.objects.filter(contact_person__is_primary=True)
  lst = []
  for campus_contact_inst in campus_contact:
    contactPerson = campus_contact_inst.contact_person
    company = contactPerson.company_contact
    values = []
    values.append(contactPerson.company_contact.id)
    values.append(contactPerson.company_contact.name)
    values.append(contactPerson.company_contact.cluster)
    values.append(contactPerson.name)
    values.append(contactPerson.designation)
    values.append(contactPerson.phone_no)
    values.append(contactPerson.email)
    values.append(contactPerson.company_contact.status)
    values.append(campus_contact_inst.last_contact)
    values.append(campus_contact_inst.student.user.name)
    comment = CompanyContactComments.objects.filter(campus_contact = campus_contact_inst).order_by('date_created')
    if comment:
      comment=comment[0].comment
    else:
      comment=""
    values.append(comment)
    values.append(campus_contact_inst.when_to_contact)
    values.append(company.id)
    values.append(company.id)
    lst.append(values[:])

  data_to_send = []

  for item in lst:
      a = []
      for x in list(item):
         try:
            if isinstance(x , datetime.date):
               df = DateFormat(x)
               dl = df.format(get_format('DATE_FORMAT'))
               a.append(str(dl))
            else:
               a.append(str(x))
         except UnicodeEncodeError:
            a.append('')
      data_to_send.append(a)

  return render_to_response('placement/placement_mgr.html',{
          'excel_form' : form,
          'assign_form' : assign_form,
          'contactperson_data': data_to_send
        },context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator', 'Placement Manager']).exists() , login_url=login_url)
def company_coordinator_today_view(request):
  user =  request.user
  if user.groups.filter(name='Company Coordinator'):
    student = user.student
    campus_contact = CampusContact.objects.filter(student=student, when_to_contact__lte=datetime.date.today())
  elif user.groups.filter(name='Placement Manager'):
    campus_contact = CampusContact.objects.filter(when_to_contact__lte=datetime.date.today())
  lst = []
  for campus_contact_inst in campus_contact:
    contactPerson = campus_contact_inst.contact_person
    values = [contactPerson.company_contact.name, contactPerson.company_contact.cluster,]
    values.append(contactPerson.name, contactPerson.designation, contactPerson.phone_no, contactPerson.email)
    values.append(contactPerson.company_contact.status)
    values.append(campus_contact_inst.last_contact)
    comment = CompanyContactComments.objects.filter(campus_contact = camous_contact_inst).order_by('date_created')[0]
    values.append(comment.comment)
    values.append(campus_contact_inst.when_to_contact)
    values.append('pk')
    values.append('pk')
    lst.append(values[:])

  data_to_send = []

  for item in lst:
      a = []
      for x in list(item):
         try:
            a.append(str(x))
         except UnicodeEncodeError:
            a.append('')
      data_to_send.append(a)

  return render_to_response('placement/company_coordi.html',{
        'contactperson_data' : data_to_send,
        }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists(), login_url=login_url)
def add_company_manual(request):
  contactpersonformset = formset_factory(ContactPersonForm, extra=2, can_delete=True)
  formset = contactpersonformset()
  companyform = AddCompanyInfoForm()
  if request.method == "POST":
    companyform = AddCompanyInfoForm(request.POST)
    formset = contactpersonformset(request.POST)
    if companyform.is_valid() and formset.is_valid():
      company = companyform.save()
      for instance in formset:
        if instance.cleaned_data:
          contactperson = ContactPerson()
          campuscontact = CampusContact()
          contactperson.name = instance.cleaned_data['name']
          contactperson.designation = instance.cleaned_data['designation']
          contactperson.phone_no = instance.cleaned_data['phone_no']
          contactperson.email = instance.cleaned_data['email']
          contactperson.company_contact = company
          if not company.contactperson_set.filter(is_primary=True):
            contactperson.is_primary = instance.cleaned_data['is_primary']
          else:
            contactperson.is_primary = False
          contactperson.save()
          campuscontact.contact_person = contactperson
          campuscontact.student = instance.cleaned_data['student'].student
          campuscontact.when_to_contact = instance.cleaned_data['when_to_contact']
          campuscontact.last_contact = instance.cleaned_data['last_contact']
          campuscontact.save()
      messages.success(request, 'Contact Person successfully added')
      return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

  return render_to_response('placement/plcmgr_manual.html',{
      'companyform' : companyform,
      'contactpersonformset' : formset,
      }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists(), login_url=login_url)
def edit_company_manual(request, company_id):
  contactpersonformset = formset_factory(ContactPersonForm, extra=2, can_delete=True)
  formset = contactpersonformset()
  companyform = AddCompanyInfoForm()
  # Add functions definition to edit
  contactpersonformset = formset_factory(ContactPersonForm, extra=1, can_delete=True)
  company = CompanyContactInfo.objects.get(id=company_id)
  companyform = AddCompanyInfoForm(instance=company)
  contact_persons = ContactPerson.objects.filter(company_contact = company)
  formset = contactpersonformset(initial=[
      {'name': x.name,
       'designation': x.designation,
       'phone_no': x.phone_no,
       'email': x.email,
       'is_primary': x.is_primary,
       'student': x.campuscontact.student,
       'last_contact': x.campuscontact.last_contact,
       'when_to_contact': x.campuscontact.when_to_contact,
      } for x in contact_persons])

  if request.method == "POST":
    companyform = AddCompanyInfoForm(request.POST, instance=company)
    formset = contactpersonformset(request.POST)
    if companyform.is_valid() and formset.is_valid():
      company = companyform.save()
      contactpersons = ContactPerson.objects.filter(company_contact=company)
      for contactperson in contactpersons:
        contactperson.campuscontact.delete()
        contactperson.delete()
      for instance in formset:
        if instance.cleaned_data:
          if instance.cleaned_data['DELETE']:
            continue
          contactperson = ContactPerson()
          campuscontact = CampusContact()
          contactperson.name = instance.cleaned_data['name']
          contactperson.designation = instance.cleaned_data['designation']
          contactperson.phone_no = instance.cleaned_data['phone_no']
          contactperson.email = instance.cleaned_data['email']
          contactperson.company_contact = company
          if not company.contactperson_set.filter(is_primary=True):
            contactperson.is_primary = instance.cleaned_data['is_primary']
          else:
            contactperson.is_primary = False
          contactperson.save()
          campuscontact.contact_person = contactperson
          campuscontact.student = instance.cleaned_data['student'].student
          campuscontact.when_to_contact = instance.cleaned_data['when_to_contact']
          campuscontact.last_contact = instance.cleaned_data['last_contact']
          campuscontact.save()
      messages.success(request, 'Contact Person successfully added')
      return HttpResponseRedirect(reverse('placement.views_img.edit_company_manual', kwargs={'company_id':company.id}))
  
  return render_to_response('placement/plcmgr_manual.html',{
      'companyform' : companyform,
      'contactpersonformset' : formset,
      }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
def add_company_coordinator(request):
  if request.method == 'POST':
    form = AddCoordinatorForm(request.POST)
    if form.is_valid():
      company_coordinator_person =  form.cleaned_data['enroll'].strip()[:8]
      user=User.objects.get(username=company_coordinator_person)
      g = Group.objects.get(name='Company Coordinator')
      g.user_set.add(user)
      messages.success(request, 'Company Coordinator added successfully')
      return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

  else:
    form = AddCoordinatorForm()
  return render_to_response('placement/add_coordinator.html',{
      'form': form,
      }, context_instance = RequestContext(request))

@login_required
def person_search(request):
  if request.is_ajax():
    q = request.GET.get('term','')
    print q
    persons = Student.objects.filter(Q(user__name__icontains = q)|Q(user__username__icontains = q),passout_year=None).order_by('-user__username')[:50]
    if not persons:
      obj = [{
        'id':'00000000',
        'label':'No results found',
        'value':q,
      }]
      data = simplejson.dumps(obj)
      return HttpResponse(data,'application/json')
    def person_dict(student):
      return {
        'id':str(student.user.username),
        'label':str(student.user.name)+" ( "+str(student.user.info)+" )",
        'value':str(student.user.name),
      }
    data = simplejson.dumps(map(person_dict,persons))
  else:
    data = 'fail'
  return HttpResponse(data,'application/json')

def assign_campus_contact(request):
#TODO: No Use, Remove this form later
  if request.method == 'POST':
    form = AssignCoordinatorForm(request.POST)
    if form.is_valid():
      company_coordinator = form.cleaned_data['company_coordinator']
      if not company_coordinator:
        messages.error(request, 'Please select Company Coordinator to assign companies')
        return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))
      if company_coordinator not in Group.objects.get(name='Company Coordinator').user_set.all():
        messages.error(request, 'Given person is not Company Coordinator. You can add using Add Company Coordinator Form')
        return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))
      try:
        assigns = form.data['assigns']
      except KeyError as e:
        messages.error(request, 'Please select comapny to assign')
        return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))
      try:
        for assign in assigns:
          company = Company.objects.get(id=assign)
          campus_contact_list = CampusContact.objects.filter(contact_person__company_contact=company)
          for campus_contact in campus_contact_list:
            campus_contact.student = company_coordinator.student
            campus_contact.save()
      except:
        messages.error(request, 'Invalid Company')
        return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))
    return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager', 'Company Coordinator']).exists() , login_url=login_url)
def contactmanager_delete(request, company_id):
  try:
    company = CompanyContactInfo.objects.get(id=company_id)
    if not request.user.groups.filter(name='Placement Manager'):
      if campus_contact.student != request.user.student:
        messages.error(request, 'You are not allowed to delete campus contact that you are not assigned. Contact Placement Manager for access')
        return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))

  except ObjectDoesNotExist:
    messages.error(request, 'The company has been already deleted')
    if not request.user.groups.filter(name="Placement Manager"):
      return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))
    return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

  contact_persons = company.contactperson_set.all()
  for contact_person in contact_persons:
    comments = contact_person.campuscontact.companycontactcomments_set.all()
    for comment in comments:
      comment.delete()
    contact_person.campuscontact.delete()
    contact_person.delete()
  company.delete()
  if not request.user.groups.filter(name="Placement Manager"):
    return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))
  return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager', 'Company Coordinator']).exists() , login_url=login_url)
def company_details(request, company_id):
  try:
    company = CompanyContactInfo.objects.get(id=company_id)
  except ObjectDoesNotExist:
    messages.error(request, 'Company is either removed or invalid')
    return HttpRequestRedirect(reverse('placement.views_img.placement_manager_view'))
  contactpersons = company.contactperson_set.all().order_by('is_primary')
  return render_to_response('placement/placement_mgr_details.html',{
      'contactpersons': contactpersons,
      'company': company,
      }, context_instance = RequestContext(request))
