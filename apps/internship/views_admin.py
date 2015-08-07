from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext 
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.db.models import Min, Count, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from zipfile import ZipFile
from django.contrib import messages

import datetime
import os, xlwt
import logging

import cStringIO as StringIO
from internship.models import *
from internship import forms 
from internship.views import resume, resume_to_verify
from placement.utils import get_resume_binary
from internship.utils import handle_exc
from nucleus.models import Student, Branch, StudentInfo
from placement.models import InternshipInformation, ProjectInformation, EducationalDetails
from placement.policy import current_session_year

from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/internship/'

l = logging.getLogger('internship')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def company_add(request) :
  """
  Add a company (for Admin)
  """
  try:
    if request.method == 'POST' :
      form = forms.CompanyForm(request.POST, request.FILES)
      if form.is_valid() :
        l.info(request.user.username +': trying to add company')
        instance = form.save(commit = False)
        # Generate the placement year dynamically from current date.
        # Year will have a value equal to the year in which placement session started.
        # Session will start from the first day of July.
        instance.year = current_session_year()
        instance.save()
        form.save_m2m()
        messages.success(request, "Company added successfully.")
        l.info(request.user.username +': added company successully.')
        return HttpResponseRedirect('/internship/company/')
      else:
        l.info(request.user.username +': form error while trying to add company')
        messages.error(request, form.errors, extra_tags='form_error')
    else:
      form = forms.CompanyForm(auto_id='%s')
    form.fields['open_for_disciplines'].help_text = None 
    return render_to_response('internship/basic_form.html', {
        'form' : form,
        'action' : '/internship/company/add/'
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username +': encountered exception when adding company')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def company_delete(request, company_id) :
  """
    Deletes a company. Asks for confirmation later (using Javascript)
  """
  try:  
    year = current_session_year()
    try:
      company = Company.objects.get(id = company_id, year = current_session_year())
    except Company.DoesNotExist as e:
      l.info(request.user.username +': trying to delete company which doesnt exist')
      return render_to_response('internship/company_list_admin.html', {
          'error_msg' : 'Company does NOT exist.',
          }, context_instance = RequestContext(request))
    l.info(request.user.username +': trying to delete company '+str(company.name_of_company))
    company.delete()
    messages.success(request, "Company delete successful")
    l.info(request.user.username +': deleted company successfully.')
    return HttpResponseRedirect('/internship/company/')
  except Exception as e:
    l.info(request.user.username + ": encoutered an error while company deletion")
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def company_list_admin(request) :
  """
    Company List as shown to the admin.
  """
  try:
    l.info(request.user.username +': trying to view company list')
    year = current_session_year()
    companies = Company.objects.filter(year = year)
    return render_to_response('internship/company_list_admin.html', {
        'companies' : companies
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username+': encountered error while viweing company list')
    l.exception(e)
    return handle_exc(e, request)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def company_edit(request, company_id) :
  """
    Edit details of an existing Company
  """
  try:
    try:
      company = Company.objects.get(id = company_id, year = current_session_year())
    except Company.DoesNotExist as e:
      l.info(request.user.username +': trying to edit company which does not exist')
      return render_to_response('internship/company_list_admin.html', {
          'error_msg' : 'Company does NOT exist.',
          }, context_instance = RequestContext(request))
    l.info(request.user.username +': trying to edit company '+str(company.name_of_company))
    if request.method == 'POST' :
      form = forms.CompanyForm(request.POST, request.FILES, instance = company)
      if form.is_valid() :
        form.save()
        messages.success(request, "Company edit was successful")
        l.info(request.user.username +': edited company successfully '+str(company.name_of_company))
        return HttpResponseRedirect('/internship/company/')
      else:
        l.info(request.user.username +': form error in company edit.')
        messages.error(request, form.errors, extra_tags='form_error')
    else :
      form = forms.CompanyForm(instance = company)
      if company.brochure :
        # Change the url of brochure
        company.brochure.name = u'internship/brochures/' + unicode(company.id) + '/'
    # Remove the default help text for a ManyToManyFeild
    form.fields['open_for_disciplines'].help_text = None
    return render_to_response('internship/basic_form.html', {
        'form' : form,
        'action' : '/internship/company/' + company_id + '/'
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ": encountered exception while edititng company.")
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').count() != 0, login_url='/nucleus/login/')
def applications_to_company(request, company_id) :
  """
    Checks the applications to a company. For admin.
  """
  try:
    if request.method == 'POST' :
      CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(status='FIN')
      l.info(request.user.username + ": Finalising Applications.")
      messages.success(request, "Selected applications finalised")
      return HttpResponseRedirect(reverse('internship.views_admin.applications_to_company', args=(company_id)))
    else:
      try:
        company = Company.objects.get(id = company_id, year = current_session_year())
        l.info(request.user.username + ": Opened view to finalise applications for "+str(company.name_of_company))
      except Company.DoesNotExist as e:
        return render_to_response('internship/company_list_admin.html', {
            'error_msg' : 'Company does NOT exist.',
            }, context_instance = RequestContext(request))
      applications = CompanyApplicationMap.objects.filter(company = company, status = 'APP')
      StudentInfo_list = []
      for application in applications :
        internship_person = application.student
        student = internship_person.student
        try:
          StudentInfo_list.append(StudentInfo.objects.get(student = student))
        except StudentInfo.DoesNotExist :
          StudentInfo_list.append(None)
      details = zip (applications, StudentInfo_list) 
      return render_to_response('internship/applications_to_company.html', {
          'details' : details,
          'company' : company,
          'task' : 'finalize',
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ": encountered error while selecting applications to companies.")
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def unfinalize(request, company_id, degree = 'UG') :
  """
  Unfinalize some finalized students of a company.
  """
  try:
    if request.method == 'POST' :
      CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(status='APP')
      l.info(request.user.username + ": Unfinalising Applications.")
      messages.success(request, "Selected applications unfinalised")
      return HttpResponseRedirect(reverse('internship.views_admin.unfinalize', args=(company_id, degree)))
    else:
      try:
        company = Company.objects.get(id = company_id, year = current_session_year())
        l.info(request.user.username + ": Opened view to unfinalise applications for "+str(company.name_of_company))
      except Company.DoesNotExist as e:
        return render_to_response('internship/company_list_admin.html', {
            'error_msg' : 'Company does NOT exist.',
            }, context_instance = RequestContext(request))
      applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN')
      StudentInfo_list = []
      for application in applications :
        internship_person = application.student
        student = internship_person.student
        try:
          StudentInfo_list.append(StudentInfo.objects.get(student = student))
        except StudentInfo.DoesNotExist :
          StudentInfo_list.append(None)
      details = zip (applications, StudentInfo_list) 
      return render_to_response('internship/applications_to_company.html', {
          'details' : details,
          'company' : company,
          'task' : 'unfinalize',
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ": encountered error while selecting applications to companies.")
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def selected_students(request, company_id) :
  """
  Download an excel file of students who has been finalized for the company in XLS format.
  """
  try:
    try:
      company = Company.objects.get(id = company_id, year = current_session_year())
    except Company.DoesNotExist as e:
      l.info(request.user.username + ": trying to download XLS sheet for finalised applications for company that does not exist")
      return render_to_response('internship/company_list_admin.html', {
          'error_msg' : 'Company does NOT exist.',
          }, context_instance = RequestContext(request))
    l.info(request.user.username + ": Downloading XLS sheet for finalised applications for "+str(company.name_of_company))
    applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN')
    if not applications : # no application has been finalized
      return HttpResponse('No student has been finalized for '+company.name_of_company)
    response = HttpResponse(content_type='application/ms-excel')
    # TODO : Format the date and time properly and set the file size in the response
    response['Content-Disposition'] = 'attachment; filename=' + company.name_of_company.replace(' ','-').replace(',','') + '_Applications.xls'
    wbk = xlwt.Workbook()
    heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
    sheet = wbk.add_sheet('Finalized students')
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 11, 'Students finalized for \'' + company.name_of_company + '\' as on ' + datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p'), heading_xf)
    headers = ('S.No.', 'Enrollment No', 'Name', 'Course', 'Year', 'Discipline', 'Gender', 'Date of Birth', 'Category', 'CGPA', 'Tenth Marks', 'Twelfth Marks', 'Contact No', 'Email ID', 'Permanent Address')
    for (col, heading) in enumerate(headers) :
      sheet.write(2, col, heading, heading_xf)
    for (row, application) in enumerate(applications) :
      row += 3
      student = application.student.student
      sheet.write(row, 0, row-2)
      sheet.write(row, 1, student.user.username)
      sheet.write(row, 2, student.user.name)
      sheet.write(row, 3, student.branch.degree)
      sheet.write(row, 4, student.semester[-2:][0:1])
      sheet.write(row, 5, student.branch.name)
      sheet.write(row, 6, student.user.get_gender_display())
      try :
        info = StudentInfo.objects.get(student = student)
        sheet.write(row, 7, student.user.birth_date.strftime('%b. %d, %Y'))
        sheet.write(row, 8, info.get_category_display())
        sheet.write(row, 14, info.permanent_address)
      except StudentInfo.DoesNotExist :
        sheet.write(row, 7, '-')
        sheet.write(row, 8, '-')
        sheet.write(row, 14, '-')
      sheet.write(row, 9, EducationalDetails.objects.get(student = student, course = previous_sem(student.semester)).cgpa)
      try :
        tenth_marks = EducationalDetails.objects.get(student = student, course = '10TH')
        sheet.write(row, 10, tenth_marks.cgpa)
      except EducationalDetails.DoesNotExist :
        sheet.write(row, 10, '-')
      except :
        sheet.write(row, 10, '-')
      try :
        twelfth_marks = EducationalDetails.objects.get(student = student, course = '12TH')
        sheet.write(row, 11, twelfth_marks.cgpa)
      except EducationalDetails.DoesNotExist :
        sheet.write(row, 11, '-')
      except :
        sheet.write(row, 11, '-')
      sheet.write(row, 12, student.user.contact_no)
      sheet.write(row, 13, student.user.email)
    wbk.save(response)
    return response
  except Exception as e:
    l.info(request.user.username + ': encountered error while downloading excel file of finalised students')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def resume_archive(request, company_id) :
  """
  Download resumes of students who has been finalized for the company in a zip file.
  """
  try:
    try:
      company = Company.objects.get(id = company_id, year = current_session_year())
    except Company.DoesNotExist as e:
      l.info(request.user.username + ': trying to download resume archive of finalised students for company that does not exist')
      return render_to_response('internship/company_list_admin.html', {
          'error_msg' : 'Company does NOT exist.',
          }, context_instance = RequestContext(request))
    l.info(request.user.username + ': downloading resume archive of finalised students for '+str(company.name_of_company))
    applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN')
    in_memory = StringIO.StringIO()
    zip = ZipFile(in_memory, 'a')
    for application in applications :
      student = application.student.student
      filepath = os.path.join(settings.MEDIA_ROOT, 'internship', 'applications',
                              'company'+str(company_id), str(student.user.username)+'.pdf')
      arcname = student.branch.code + student.branch.degree + student.user.name + '.pdf'
      zip.write(filepath, arcname)
    if not applications : # no application has been finalized
      return HttpResponse('No student has been finalized for '+company.name_of_company)
    zip.close()
    in_memory.seek(0)
    response = HttpResponse(in_memory.read(), content_type="application/x-zip-compressed")
    # TODO : Sanitize the name of company as it may cause error due to presence of certain characters
    response['Content-Disposition'] = 'attachment; filename=' + company.name_of_company + '_Resumes.zip'
    response['Content-Length'] = in_memory.tell()
    return response
  except Exception as e:
    l.info(request.user.username + ": error while downloading resumes of students who has been fianlised for the company in zip.")
    l.exception(e)
    return handle_exc(e, request)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def branch_details(request, branch_code = None) :
  """
  Display list of students in a branch. If no branch is specified, it displays
  list of all the branches.
  """
  try :
    if branch_code == None :
      l.info(request.user.username + ': Viewing Branch Details')
      # Display a list of branches
      internship_persons = InternshipPerson.objects.filter(status = 'OPN')
      branch_codes = internship_persons.values_list('student__branch__code').distinct()
      branches = Branch.objects.filter(code__in = branch_codes).order_by('degree')
      return render_to_response('internship/branch_details_list.html', {
          'branches' : branches,
          }, context_instance = RequestContext(request))
    # Display list of students in the specified branch
    branch = get_object_or_404(Branch, code = branch_code)
    l.info(request.user.username + ': Viewing Students of ' + branch.name)
    internship_persons = InternshipPerson.objects.filter(student__branch = branch, status = 'OPN', student__passout_year = None).order_by('student__user__name')
    details = []
    # TODO : Put all these queries into one per model
    educational_details = EducationalDetails.objects.all()
    person_info_all = StudentInfo.objects.all()
    apps = CompanyApplicationMap.objects.all()
    for internship_person in internship_persons:
      student = internship_person.student
      try :
        tenth_marks = educational_details.get(student = student, course = '10TH').cgpa
      except EducationalDetails.DoesNotExist :
        tenth_marks = '-'
      try :
        twelfth_marks = educational_details.get(student = student, course = '12TH').cgpa
      except EducationalDetails.DoesNotExist :
        twelfth_marks = '-'
      graduation_marks = educational_details.filter(student = student, course = 'UG0')
      if graduation_marks:
        graduation_marks = graduation_marks[0].cgpa
      else:
        graduation_marks = '-'
      try :
        student_info = person_info_all.get(student = student)
      except StudentInfo.DoesNotExist :
        student_info = None
      applications = apps.filter(student = internship_person)
      if applications:
        no_of_applications = applications.count()
        last_application = applications[0]
      else :
        no_of_applications = 0
        last_application = "-"
      details.append((internship_person,tenth_marks,twelfth_marks,graduation_marks, student_info, no_of_applications, last_application))
    return render_to_response('internship/branch_details.html', {
          'branch' : branch,
          'details' : details
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when viewing branch details')
    l.exception(e)
    return handle_exc(e, request)


