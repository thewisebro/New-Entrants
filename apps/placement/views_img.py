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
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
def placement_manager_view(request):
  assign_form = AssignCoordinatorForm()
  coordinator_work_form = ViewCoordinatorWorkForm()
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
  return render_to_response('placement/placement_mgr.html',{
          'excel_form' : form,
          'assign_form' : assign_form,
          'coordinator_work': coordinator_work_form,
        },context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
def placement_manager_contact_person_data(request):
  company = CompanyContactInfo.objects.all()
  contactPerson_lst = ContactPerson.objects.all()
  comment_lst = CompanyContactComments.objects.all()
  lst = []
  for company_inst in company:
    if ContactPerson.objects.filter(company_contact=company_inst):
      contact_exist = True
      try:
       contactPerson = contactPerson_lst.get(company_contact=company_inst, is_primary = True)
      except:
       contactPerson = contactPerson_lst.filter(company_contact=company_inst).order_by('name')[0]
    else:
      contact_exist = False
      contactPerson = ContactPerson()
      contactPerson.name = "Not Defined"
      contactPerson.designation = ""
      contactPerson.phone_no = ""
      contactPerson.email = ""
    values = []
    values.append(company_inst.id)
    values.append(company_inst.name)
    values.append(company_inst.cluster)
    values.append(contactPerson.name)
    values.append(contactPerson.designation)
    values.append(contactPerson.phone_no)
    values.append(contactPerson.email)
    values.append(company_inst.status)
    if contact_exist:
      values.append(contactPerson.campuscontact.last_contact)
      try:
        values.append(contactPerson.campuscontact.student.user.name)
      except:
        values.append("None")
      comment = comment_lst.filter(campus_contact = contactPerson.campuscontact).order_by('-date_created')
      if comment:
        comment_text=comment[0].comment
        if comment_text == "":
          comment_text = "None"
      else:
        comment_text="None"
    else:
      values.append("")
      values.append("")
      comment_text=""
    values.append(comment_text)
    values.append(contactPerson.campuscontact.when_to_contact if contact_exist else "")
    values.append(company_inst.id)
    values.append(company_inst.id)
    values.append(company_inst.id)
    lst.append(values[:])
  data_to_send = []
  for item in lst:
      a = []
      for x in list(item):
         try:
            if isinstance(x , datetime.date):
               df = DateFormat(x)
               dl = df.format('d/m/Y')
               a.append(str(dl))
            elif list(item).index(x) == 8:
               try:
                 y = x.split("-")
                 if len(y)==3:
                   z = [int(i) for i in y]
                   date=datetime.date(z[0],z[1],z[2])
                   string_date=date.strftime("%d/%m/%Y")
                   a.append(string_date)
                 else:
                   a.append(x)
               except:
                 a.append(x)
            else:
               a.append(str(x))
         except UnicodeEncodeError:
            a.append('')
      data_to_send.append(a)
  data_to_send = {'data':data_to_send}
  return HttpResponse(simplejson.dumps(data_to_send),'application/json')

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator', 'Placement Manager']).exists() , login_url=login_url)
def company_coordinator_view(request,user_id=None):
  if user_id:
    return render_to_response('placement/company_coordi.html',{'user_id':user_id},context_instance = RequestContext(request))
  return render_to_response('placement/company_coordi.html',context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator','Placement Manager']).exists(), login_url=login_url)
def company_coordinator_contact_person_data(request,user_id=None):
  if request.user.groups.filter(name="Placement Manager").exists():
    if user_id:
      user = User.objects.get(id=user_id)
    elif request.user.groups.filter(name="Company Coordinator").exists():
      user = request.user
  else:
    user =  request.user

  student = user.student
  campus_contacts = CampusContact.objects.filter(student = student, contact_person__is_primary=True).order_by('contact_person__company_contact','-contact_person__is_primary')
  contact_persons = [cc.contact_person for cc in campus_contacts]
  company = [cp.company_contact for cp in contact_persons]

  lst = []
  for company_inst in company:
    if ContactPerson.objects.filter(company_contact=company_inst):
      contact_exist = True
      try:
        contactPerson = ContactPerson.objects.get(company_contact=company_inst, is_primary = True)
      except:
        contactPerson = ContactPerson.objects.filter(company_contact=company_inst).order_by('name')[0]
    else:
      contact_exist = False
      contactPerson = ContactPerson()
      contactPerson.name = "Not Defined"
      contactPerson.designation = ""
      contactPerson.phone_no = ""
      contactPerson.email = ""
    values = []
    values.append(company_inst.name)
    values.append(company_inst.cluster)
    values.append(contactPerson.name)
    values.append(contactPerson.designation)
    values.append(contactPerson.phone_no)
    values.append(contactPerson.email)
    values.append(company_inst.status)
    if contact_exist:
      values.append(contactPerson.campuscontact.last_contact)
      try:
        values.append(contactPerson.campuscontact.student.user.name)
      except:
        values.append("None")
      comment = CompanyContactComments.objects.filter(campus_contact = contactPerson.campuscontact).order_by('-date_created')
      if comment:
        comment_text=comment[0].comment
        if comment_text == "":
          comment_text = "None"
      else:
        comment_text="None"
    else:
      values.append("")
      values.append("")
      comment_text=""
    values.append(comment_text)
    values.append(contactPerson.campuscontact.when_to_contact if contact_exist else "")
    values.append(company_inst.id)
    values.append(company_inst.id)
    values.append(company_inst.id)
    lst.append(values[:])

  data_to_send = []

  for item in lst:
      a = []
      for x in list(item):
         try:
            if isinstance(x , datetime.date):
               df = DateFormat(x)
               dl = df.format('d/m/Y')
               a.append(str(dl))
            elif list(item).index(x) == 7:
               try:
                 y = x.split("-")
                 if len(y)==3:
                   z = [int(i) for i in y]
                   date=datetime.date(z[0],z[1],z[2])
                   string_date=date.strftime("%d/%m/%Y")
                   a.append(string_date)
                 else:
                   a.append(x)
               except:
                 a.append(x)
            else:
               a.append(str(x))
         except UnicodeEncodeError:
            a.append('')
      data_to_send.append(a)
  data_to_send = {'data':data_to_send}
  return HttpResponse(simplejson.dumps(data_to_send),'application/json')

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator']).exists() , login_url=login_url)
def company_coordinator_today_view(request):
  return render_to_response('placement/company_coordi.html',{
        'today' : True,
        }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator']).exists() , login_url=login_url)
def company_coordinator_contact_person_data_today(request):
  user =  request.user
  student = user.student
  campusContact_lst = CampusContact.objects.filter(student=student, when_to_contact__lte=datetime.datetime.today()).order_by('-contact_person__company_contact','-contact_person__is_primary')
  lst = []
  for campus_contact_inst in campusContact_lst:
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
    try:
      values.append(campus_contact_inst.student.user.name)
    except:
      values.append("None")
    comment = CompanyContactComments.objects.filter(campus_contact = campus_contact_inst).order_by('-date_created')
    if comment:
      comment_text=comment[0].comment
      if comment_text=="":
        comment_text = "None"
    else:
      comment_text="None"
    values.append(comment)
    values.append(campus_contact_inst.when_to_contact)
    values.append(contactPerson.company_contact.id)
    values.append(contactPerson.company_contact.id)
    values.append(campus_contact_inst.id)
    lst.append(values[:])

  data_to_send = []

  for item in lst:
      a = []
      for x in list(item):
         try:
            if isinstance(x , datetime.date):
               df = DateFormat(x)
               dl = df.format('d/m/Y')
               a.append(str(dl))
            elif list(item).index(x) == 7:
               try:
                 y = x.split("-")
                 if len(y)==3:
                   z = [int(i) for i in y]
                   date=datetime.date(z[0],z[1],z[2])
                   string_date=date.strftime("%d/%m/%Y")
                   a.append(string_date)
                 else:
                   a.append(x)
               except:
                 a.append(x)
            else:
               a.append(str(x))
         except UnicodeEncodeError:
            a.append('')
      data_to_send.append(a)
  data_to_send = {'data':data_to_send}
  return HttpResponse(simplejson.dumps(data_to_send),'application/json')




@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator','Placement Manager']).exists(), login_url=login_url)
def add_company_manual(request):
#TODO: Throw error when contact person is defined but campus contact is not
#TODO_Before production: Add first contact as Primary Contact if none defined

  a = request.user.groups.filter(name='Placement Manager')
  if not a:
    contactpersonformset = formset_factory(ContactPersonForm, extra=1, can_delete=True)
    formset = contactpersonformset(initial=[{'student':request.user}])
  else:
    contactpersonformset = formset_factory(ContactPersonForm, extra=2, can_delete=True)
    formset = contactpersonformset()

  if not a:
    for form in formset:
      form.fields['student'].widget.attrs['disabled'] = True

  companyform = AddCompanyInfoForm()
  if request.method == "POST":
    companyform = AddCompanyInfoForm(request.POST)
    formset = contactpersonformset(request.POST)
    if companyform.is_valid() and formset.is_valid():
      company = companyform.save(commit=False)
      contactPersons = []
      campusContacts = []
      for instance in formset:
        if instance.cleaned_data:
          contactperson = ContactPerson()
          campuscontact = CampusContact()
          contactperson.name = instance.cleaned_data['name']
          contactperson.designation = instance.cleaned_data['designation']
          contactperson.phone_no = instance.cleaned_data['phone_no']
          contactperson.email = instance.cleaned_data['email']
          contactperson.company_contact = company
          contactperson.is_primary = instance.cleaned_data['is_primary']
          contactPersons.append(contactperson)
          campuscontact.contact_person = contactperson
          if not a:
            campuscontact.student = request.user.student
          else:
            campuscontact.student = instance.cleaned_data['student'].student
          if instance.cleaned_data['last_contact']:
            campuscontact.last_contact = datetime.date.today()
          campuscontact.when_to_contact = instance.cleaned_data['when_to_contact']
          campusContacts.append(campuscontact)
      ## To check whether multiple primary added or not
      is_primary_add = False
      for contactPerson in contactPersons:
        if contactPerson.is_primary and is_primary_add:
          messages.error(request, "Multiple Primary persons added")
          return HttpResponseRedirect(reverse('placement.views_img.add_company_manual'))
        elif contactPerson.is_primary and not is_primary_add:
          is_primary_add = True
      if not is_primary_add:
        messages.error(request, "Please select at least one primary contact")
        return HttpResponseRedirect(reverse('placement.views_img.add_company_manual'))
      # Everything is good. Commit all contact persons and campus contacts
      company.save()
      for i in range(len(contactPersons)):
        contactPersons[i].company_contact = company
        contactPersons[i].save()
        campusContacts[i].contact_person = contactPersons[i]
        campusContacts[i].save()

      messages.success(request, 'Company successfully added')
      return HttpResponseRedirect(reverse('nucleus.views.close_dialog',kwargs={'dialog_name':'company_details_dialog'}))

  return render_to_response('placement/plcmgr_manual.html',{
      'companyform' : companyform,
      'contactpersonformset' : formset,
      }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager','Company Coordinator']).exists(), login_url=login_url)
def edit_company_manual(request, company_id):
  if not request.user.groups.filter(name="Placement Manager") and (not CampusContact.objects.filter(student=request.user.student, contact_person__company_contact__id=company_id)):
    messages.error(request, "You don't have permission to edit this company")
    return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))
  a = request.user.groups.filter(name='Placement Manager')
  if not a:
    contactpersonformset = formset_factory(ContactPersonForm, extra=1, can_delete=True)
    formset = contactpersonformset(initial=[{'student':request.user},{'student':request.user},])
  else:
    contactpersonformset = formset_factory(ContactPersonForm, extra=2, can_delete=True)
    formset = contactpersonformset()
  companyform = AddCompanyInfoForm()
  #Add functions definition to edit
  contactpersonformset = formset_factory(ContactPersonForm, extra=1, can_delete=True)
  company = CompanyContactInfo.objects.get(id=company_id)
  companyform = AddCompanyInfoForm(instance=company)
  contact_persons = ContactPerson.objects.filter(company_contact = company)
  try:
    formset = contactpersonformset(initial=[
      {'name': x.name,
       'designation': x.designation,
       'phone_no': x.phone_no,
       'email': x.email,
       'contact_id': x.id,
       'is_primary': x.is_primary,
       'student': x.campuscontact.student,
       'when_to_contact': x.campuscontact.when_to_contact,
      } for x in contact_persons])
  except:
    formset = contactpersonformset(initial=[
      {'name': x.name,
       'designation': x.designation,
       'phone_no': x.phone_no,
       'email': x.email,
       'contact_id': x.id,
       'is_primary': x.is_primary,
       'student': "None",
       'when_to_contact': x.campuscontact.when_to_contact,
      } for x in contact_persons])

  if not a:
    for form in formset:
      form.fields['student'].widget.attrs['disabled'] = True

  if request.method == "POST":
    companyform = AddCompanyInfoForm(request.POST, instance=company)
    formset = contactpersonformset(request.POST)
    if companyform.is_valid() and formset.is_valid():
      company = companyform.save()

      is_primary_changed = False
      is_primary_delete = False
      for instance in formset:
        if 'contact_id' in instance.changed_data:
          messages.error(request, 'Invalid Contact to change')
          return HttpResponseRedirect(reverse('nucleus.views.close_dialog',kwargs={'dialog_name':'company_details_dialog'}))
        if 'is_primary' in instance.changed_data:
          is_primary_changed = True
          if instance.cleaned_data['is_primary'] and instance.cleaned_data['DELETE']:
            is_primary_delete = True

      if is_primary_delete:
        messages.error(request, "Please change primary contact first to delete the contact")
        return HttpResponseRedirect(reverse('placement.views_img.edit_company_manual', kwargs={'company_id':company.id}))


      if is_primary_changed:
        is_primary_add = False
        for instance in formset:
          if instance.cleaned_data:
            if is_primary_add and instance.cleaned_data['is_primary']:
              messages.error(request, "Multiple primary contacts are added")
              return HttpResponseRedirect(reverse('placement.views_img.edit_company_manual', kwargs={'company_id':company.id}))
            elif instance.cleaned_data['is_primary'] and not is_primary_add:
              is_primary_add = True

        if not is_primary_add:
          messages.error(request, "Please select at least one primary contact")
          return HttpResponseRedirect(reverse('placement.views_img.edit_company_manual', kwargs={'company_id':company.id}))
      # Everything is good. Commit all contact persons and campus contacts

      for instance in formset:
        if instance.cleaned_data:
          try:
            contactperson = ContactPerson.objects.get(id = instance.cleaned_data['contact_id'])
            campuscontact = contactperson.campuscontact
          except:
            contactperson = ContactPerson()
            campuscontact = CampusContact()
          if instance.cleaned_data['DELETE']:
            if contactperson.is_primary:
              messages.error(request, "Please change primary contact first to delete the contact")
              return HttpResponseRedirect(reverse('placement.views_img.edit_company_manual', kwargs={'company_id':company.id}))
            campuscontact.delete()
            contactperson.delete()
            continue
          contactperson.name = instance.cleaned_data['name']
          contactperson.designation = instance.cleaned_data['designation']
          contactperson.phone_no = instance.cleaned_data['phone_no']
          contactperson.email = instance.cleaned_data['email']
          contactperson.company_contact = company
          contactperson.is_primary = instance.cleaned_data['is_primary']
          contactperson.save()
          campuscontact.contact_person = contactperson
          if a:
            campuscontact.student = instance.cleaned_data['student'].student
          else:
            campuscontact.student = request.user.student

          campuscontact.when_to_contact = instance.cleaned_data['when_to_contact']
          if instance.cleaned_data['last_contact']:
            campuscontact.last_contact = datetime.date.today()
          campuscontact.save()
      messages.success(request, 'Contact Person successfully updated')
#      return HttpResponseRedirect(reverse('placement.views_img.edit_company_manual', kwargs={'company_id':company.id}))
      return HttpResponseRedirect(reverse('nucleus.views.close_dialog',kwargs={'dialog_name':'company_details_dialog'}))

  return render_to_response('placement/plcmgr_manual.html',{
      'edit_company_page': True,
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

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager', 'Company Coordinator']).exists() , login_url=login_url)
def company_search(request):
  if request.is_ajax():
    q = request.GET.get('term','')
    print q
    company = CompanyContactInfo.objects.filter(name__icontains = q).order_by('name')[:50]
    if not company:
      obj = [{
        'id':'0',
        'label':'Company Not available',
        'value':q,
      }]
      data = simplejson.dumps(obj)
      return HttpResponse(data,'application/json')
    def company_dict(company):
      try:
        return {
          'id':str(company.id),
          'label':str(company.name)+" ( "+str(company.contactperson_set.get(is_primary=True).campuscontact.student.name)+" )",
          'value':str(company.name),
        }
      except:
        return {
          'id':str(company.id),
          'label':str(company.name)+" (Unallotted)",
          'value':str(company.name),
        }

    data = simplejson.dumps(map(company_dict,company))
  else:
    data = 'fail'
  return HttpResponse(data,'application/json')

@login_required
@user_passes_test(lambda u:u.groups.filter(name='Placement Manager').exists() , login_url=login_url)
def assign_campus_contact(request):
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
        assigns = form.data.getlist('assigns')
      except KeyError as e:
        messages.error(request, 'Please select comapny to assign')
        return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))
      try:
        for assign in assigns:
          company = CompanyContactInfo.objects.get(id=assign)
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
def campuscontact_delete(request, campuscontact_id):
  try:
    campus_contact = CampusContact.objects.get(id=campuscontact_id)
    if not request.user.groups.filter(name='Placement Manager'):
      if campus_contact.student != request.user.student:
        messages.error(request, 'You are not allowed to delete campus contact that you are not assigned. Contact Placement Manager for access')
        return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))

  except ObjectDoesNotExist:
    messages.error(request, 'The contact has already been deleted')
    if not request.user.groups.filter(name="Placement Manager"):
      return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))
    return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

  if campus_contact.contact_person.is_primary:
    if len(ContactPerson.objects.filter(company_contact = campus_contact.contact_person.company_contact))==1:
      return contactmanager_delete(request, campus_contact.contact_person.compan_contact.id)
    else:
      messages.error(request, 'Can not delete primary contact.')
  else:
    contactperson = campus_contact.contact_person
    campus_contact.delete()
    contactperson.delete()
    messages.success(request, 'Contact successfully deleted')
  if not request.user.groups.filter(name="Placement Manager"):
    return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))
  return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))

@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager','Company Coordinator']).exists() , login_url=login_url)
def edit_comments(request, company_id):
#TODO: Edit comments for company coordinators as well as placement managers. Don't know how to map comments to Placement Manager
  user = request.user
  company_contact = CompanyContactInfo.objects.get(id=company_id)
  a = user.groups.filter(name='Placement Manager').exists()
  if not a:
    campus_contact_lst = CampusContact.objects.filter(student=user.student, contact_person__company_contact=company_contact).order_by('-contact_person__is_primary')
  else:
    campus_contact_lst = CampusContact.objects.filter(contact_person__company_contact = company_contact).order_by('-contact_person__is_primary')

  if request.POST:
    form = CommentsForm(request.POST, company_contact=company_contact)
    if form.is_valid():
      if not user.groups.filter(name='Company Coordinator'):
        comment_inst = form.save(commit=False)
        comment_inst.comment = "<span name="+request.user.username+" style='color:red;'>"+form.cleaned_data['comment']+"</span>"
        comment_inst.campus_contact = CampusContact.objects.get(contact_person__id=int(form.data['contact_person']))
        comment_inst.save()
      elif a and not CampusContact.objects.filter(contact_person__id=int(form.data['contact_person']), student=user.student).exists():
        comment_inst = form.save(commit=False)
        comment_inst.comment = "<span name="+request.user.username+" style='color:red;'>"+form.cleaned_data['comment']+"</span>"
        comment_inst.campus_contact = CampusContact.objects.get(contact_person__id=int(form.data['contact_person']))
        comment_inst.save()
      elif CampusContact.objects.filter(contact_person__id=int(form.data['contact_person']), student=user.student).exists():
        comment_inst = form.save(commit=False)
        comment_inst.campus_contact = CampusContact.objects.get(contact_person__id=int(form.data['contact_person']), student=user.student)
        comment_inst.save()
      else:
        messages.error(request, "You are not allowed to edit comments")
        return HttpResponse("You are not allowed to edit comments")

  else:
    form = CommentsForm(company_contact=company_contact)

  return render_to_response('placement/edit_comments.html',{
      'form': form,
      'company':company_contact,
      'campus_contacts':campus_contact_lst,
      }, context_instance = RequestContext(request))

@user_passes_test(lambda u:u.groups.filter(name__in=['Placement Manager','Company Coordinator']).exists() , login_url=login_url)
def delete_comments(request, comment_id):
  try:
    comment = CompanyContactComments.objects.get(id = comment_id)
  except CompanyContactComments.DoesNotExist:
    messages.error(request, "Comment does not exist")
    return HttpResponse("Comment does not exist")
  student = comment.campus_contact.student
  try:
    student_request = request.user.student
    isPM = False
  except AttributeError:
    isPM = True
  if not comment.comment:
    comment.delete()
    messages.success(request, "Comment deleted")
    return HttpResponseRedirect(reverse('placement.views_img.edit_comments',kwargs={'company_id':comment.campus_contact.contact_person.company_contact.id}))
  import ipdb; ipdb.set_trace()
  PM_comment = '<span name=' in comment.comment
  if isPM:
    comment.delete()
    messages.success(request, "Comment deleted")
    return HttpResponseRedirect(reverse('placement.views_img.edit_comments',kwargs={'company_id':comment.campus_contact.contact_person.company_contact.id}))

  if request.user.student==student:
    if not PM_comment:
      comment.delete()
      messages.success(request, "Comment deleted")
      return HttpResponseRedirect(reverse('placement.views_img.edit_comments',kwargs={'company_id':comment.campus_contact.contact_person.company_contact.id}))

  messages.error(request, "Access Denied")
  return HttpResponseRedirect(reverse('placement.views_img.edit_comments',kwargs={'company_id':comment.campus_contact.contact_person.company_contact.id}))


@login_required
@user_passes_test(lambda u:u.groups.filter(name__in=['Company Coordinator','Placement Manager']).exists() , login_url=login_url)
def company_details(request, company_id):
  try:
    company = CompanyContactInfo.objects.get(id=company_id)
  except ObjectDoesNotExist:
    messages.error(request, 'Company is either removed or invalid')
    if request.user.groups.filter(name='Company Coordinator'):
      return HttpResponseRedirect(reverse('placement.views_img.company_coordinator_view'))
    return HttpResponseRedirect(reverse('placement.views_img.placement_manager_view'))
  contactpersons = company.contactperson_set.all().order_by('-is_primary')
  return render_to_response('placement/placement_mgr_details.html',{
      'contactpersons': contactpersons,
      'company': company,
      }, context_instance = RequestContext(request))
