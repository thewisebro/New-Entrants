from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Min

from django.views.decorators.csrf import csrf_exempt
from zipfile import ZipFile

import cStringIO as StringIO
import logging
import os, xlwt
import datetime

import json
from django.contrib import messages

from nucleus.models import StudentInfo, Branch
from placement.forms import BaseModelFormFunction
from placement import forms
from placement.policy import current_session_year
from placement.models import *
from placement.utils import *

from django.conf import settings

l = logging.getLogger('placement')

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# IMPORTANT : Objects of Student and PlacementPerson are to be stored in session.
# These objects are used in all the templates.

def test(request):
  return render_to_response('placement/test.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def finalize(request, company_id, degree='UG') :
  """
  View applications from a degree to a company. The students are displayed using different colors to
  represent that they have been selected in some other company.
  'degree' can be a value from ('UG','PG','PHD')
  """
  try :
    l.info(request.user.username + ': Opened Applications Page for ' + company_id)
    if request.method == 'POST' :
      CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(status='FIN')
      messages.success(request, 'The selected applications are finalized for the placement procedure.')
      l.info(request.user.username + ': Redirecting to company.admin_list after finalizing applications')
      return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
    else :
      company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
      # Get applications for the company from the specified degree
      applications = []
      # Categories which are to be colored.
      # The applications are displayed in the order of the categories as specified.
      for category in (None,'C','U','B','A') :
        applications += list(CompanyApplicationMap.objects.filter(company = company,
                                                                  plac_person__person__semester__startswith = degree,
                                                                  plac_person__placed_company_category = category,
                                                                  status='APP'))
      return render_to_response('placement/applications_to_company.html', {
          'company' : company,
          'degree' : degree,
          'all_degrees' : {'UG', 'PG', 'PHD' },
          'applications' : applications,
          'task' : 'finalize',
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to view applications.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def unfinalize(request, company_id, degree = 'UG') :
  """
  Unfinalize some finalized students of a company.
  """
  if request.method == "POST" :
      CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(status='APP')
      messages.success(request, 'The selected applications are unfinalized for the placement procedure.')
      l.info(request.user.username + ': Redirecting to company.admin_list after unfinalizing applications')
      return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
  else :
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    # Get applications for the company from the specified degree
    applications = []
    # Categories which are to be colored.
    # The applications are displayed in the order of the categories as specified.
    for category in (None,'C','U','B','A') :
      applications += list(CompanyApplicationMap.objects.filter(company = company,
                                                                plac_person__person__semester__startswith = degree,
                                                                plac_person__placed_company_category = category,
                                                                status='FIN'))
    return render_to_response('placement/applications_to_company.html', {
        'company' : company,
        'degree' : degree,
        'all_degrees' : {'UG', 'PG', 'PHD' },
        'applications' : applications,
        'task' : 'unfinalize',
        }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def shortlist(request, company_id, task = None) :
  """
  Update shortlist of a company.
  """
  company = Company.objects.get(pk = company_id)
  if request.method == "POST" :
    # update shortlist
    CompanyApplicationMap.objects.filter(company = company).update(shortlisted = False)
    CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(shortlisted = True)
    l.info(request.user.username + ': updated shortlist for company ' + company_id)
    applications = CompanyApplicationMap.objects.filter(company = company, shortlisted = True)
    # now download xls list of students or zip file of resumes as per the request
    if task == "xlslist" :
      wbk = xlwt.Workbook()
      heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
      sheet = wbk.add_sheet('Finalized students')
      sheet.set_panes_frozen(True)
      sheet.set_horz_split_pos(3)
      sheet.set_remove_splits(True)
      sheet.write_merge(0, 1, 0, 11, 'Students shortlisted for \'' + company.name + '\' as on '
                        + datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p'), heading_xf)
      headers = ('S.No.', 'Enrollment No', 'Name', 'Course', 'Discipline', 'Gender',
                 'Date of Birth', 'Category', 'CGPA', 'Contact No', 'Email ID')
      for (col, heading) in enumerate(headers) :
        sheet.write(2, col, heading, heading_xf)
      for (row, application) in enumerate(applications) :
        row += 3
        student = application.plac_person.student
        info = StudentInfo.objects.get(student=student)
        if application.plac_person.is_debarred:
          style = xlwt.easyxf('font: color-index red')
        else :
          style = xlwt.easyxf()
        sheet.write(row, 0, row-2, style)
        sheet.write(row, 1, student.user.username, style)
        sheet.write(row, 2, student.name, style)
        sheet.write(row, 3, student.branch.degree, style)
        sheet.write(row, 4, student.branch.name, style)
        sheet.write(row, 5, student.get_gender_display(), style)
        sheet.write(row, 6, info.birth_date.strftime('%b. %d, %Y'), style)
        sheet.write(row, 7, info.get_category_display(), style)
        sheet.write(row, 8, student.cgpa, style)
        sheet.write(row, 9, student.personal_contact_no,style)
        sheet.write(row, 10, student.email_id, style)
      response = HttpResponse(content_type='application/ms-excel')
      response['Content-Disposition'] = 'attachment; filename=' + sanitise_for_download(company.name) + '_Applications.xls'
      wbk.save(response)
      return response
    else : # resumes' zip file
      in_memory = StringIO.StringIO()
      zip = ZipFile(in_memory, 'a')
      for application in applications :
        student = application.plac_person.student
        filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications',
                                'company'+str(company_id), str(student.user.username)+'.pdf')
        arcname = student.branch.code + '_' +  student.branch.degree + '_' + student.name + '.pdf'
        zip.write(filepath, arcname)
      if not applications : # no application has been finalized
        l.info (request.user.username + ': no applications shortlisted.')
        messages.error(request, 'No student has been finalized for ' + company.name + '.')
        return HttpResponseRedirect(reverse('placement.views.index'))
      zip.close()
      in_memory.seek(0)
      response = HttpResponse(in_memory.read(), mimetype="application/x-zip-compressed")
      response['Content-Disposition'] = 'attachment; filename=' + sanitise_for_download(company.name) + '_Resumes.zip'
      response['Content-Length'] = in_memory.tell()
      return response
  else :
    company = Company.objects.get(pk = company_id)
    applications = []
    for category in (None, 'C', 'U', 'B', 'A') :
      applications += list(CompanyApplicationMap.objects.filter(company = company,
                                                                plac_person__placed_company_category = category,
                                                                status='FIN'))
    return render_to_response('placement/shortlist.html', {
        'company' : company,
        'applications' : applications,
        }, context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def resume_archive(request, company_id) :
  """
  Download resumes of students who has been finalized for the company in a zip file.
  """
  try :
    l.info (request.user.username + ': downloading resume archive')
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN')
    in_memory = StringIO.StringIO()
    zip = ZipFile(in_memory, 'a')
    for application in applications :
      student = application.plac_person.student
      filepath = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications',
                              'company'+str(company_id), str(student.user.username)+'.pdf')
      arcname = student.branch.code + '_' +  student.branch.degree + '_' + student.name + '.pdf'
      zip.write(filepath, arcname)
    if not applications : # no application has been finalized
      l.info (request.user.username + ': no applications finalised in resume archive')
      messages.error(request, 'No student has been finalized for ' + company.name + '.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    zip.close()
    in_memory.seek(0)
    response = HttpResponse(in_memory.read(), mimetype="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=' + sanitise_for_download(company.name) + '_Resumes.zip'
    response['Content-Length'] = in_memory.tell()
    return response
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to view exceptions.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def selected_students(request, company_id) :
  """
  Download an excel file of students who has been finalized for the company in XLS format.
  """
  try :
    l.info(request.user.username + ': trying to get xls sheet of selected students')
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN')
    if not applications : # no application has been finalized
      l.info(request.user.username + ': no finalised students for xls sheet')
      messages.error(request, 'No student has been finalized for ' + company.name + '.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + sanitise_for_download(company.name) + '_Applications.xls'
    wbk = xlwt.Workbook()
    heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
    sheet = wbk.add_sheet('Finalized students')
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 11, 'Students finalized for \'' + company.name + '\' as on ' + datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p'), heading_xf)
    headers = ('S.No.', 'Enrollment No', 'Name', 'Course', 'Year', 'Discipline', 'Gender', 'Date of Birth', 'Category', 'CGPA', 'Tenth Marks', 'Twelfth Marks', 'Graduation Marks', 'Discipline(UG)', 'College(UG)','Contact No', 'Email ID', 'Permanent Address')
    for (col, heading) in enumerate(headers) :
      sheet.write(2, col, heading, heading_xf)
    for (row, application) in enumerate(applications) :
      row += 3
      student = application.plac_person.student
      if application.plac_person.is_debarred:
        style = xlwt.easyxf('font: color-index red')
      else :
        style = xlwt.easyxf()
      sheet.write(row, 0, row-2, style)
      sheet.write(row, 1, student.user.username, style)
      sheet.write(row, 2, student.name, style)
      sheet.write(row, 3, student.branch.degree, style)
      sheet.write(row, 4, student.semester[-2:][0:1], style)
      sheet.write(row, 5, student.branch.name, style)
      sheet.write(row, 6, student.get_gender_display(), style)
      try :
        info = StudentInfo.objects.get(student = student)
        try:
          sheet.write(row, 7, info.birth_date.strftime('%b. %d, %Y'), style)
        except Exception as e:
          sheet.write(row, 7, '-', style)
        sheet.write(row, 8, info.get_category_display(), style)
        sheet.write(row, 17, info.permanent_address, style)
      except StudentInfo.DoesNotExist :
        sheet.write(row, 7, '-', style)
        sheet.write(row, 8, '-', style)
        sheet.write(row, 17, '-', style)
      sheet.write(row, 9, student.cgpa, style)
      try :
        tenth_marks = EducationalDetails.objects.get(student = student, course = '10TH')
        sheet.write(row, 10, tenth_marks.cgpa, style)
      except:
        sheet.write(row, 10, '-', style)
      try :
        twelfth_marks = EducationalDetails.objects.get(student = student, course = '12TH')
        sheet.write(row, 11, twelfth_marks.cgpa, style)
      except:
        sheet.write(row, 11, '-', style)
      try :
        try:
          graduation_marks = EducationalDetails.objects.get(student = student, course = 'UG0')
        except:
          graduation_marks = EducationalDetails.objects.filter(student = student, course = 'UG0')[0]
        sheet.write(row, 12, graduation_marks.cgpa, style)
        if graduation_marks.discipline == 'NOT':
          grad_disc = graduation_marks.discipline_provided
        elif graduation_marks.discipline == 'NA':
          grad_disc = 'Not Applicable'
        else :
          branch = Branch.objects.filter(pk = graduation_marks.discipline)[0]
          grad_disc = branch.name
        sheet.write(row, 13, grad_disc, style)
        sheet.write(row, 14, graduation_marks.institution, style)
      except:
        sheet.write(row, 12, '-', style)
        sheet.write(row, 13, '-', style)
        sheet.write(row, 14, '-', style)
      sheet.write(row, 15, student.personal_contact_no,style)
      sheet.write(row, 16, student.email_id, style)
    wbk.save(response)
    return response
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to view xls sheet')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def cpt(request, year = None) :
  """
  View details of all the CPT members
  """
  try :
    current_session = current_session_year()
    if year :
      year = int(year)
    else :
      year = current_session
    l.info (request.user.username + ': viewing details of all CPT members for year ' + str(year))
    year_min = CPTMember.objects.aggregate(min = Min('year'))['min']
    if not year_min :
      year_min = current_session
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = []
    for i in range(year_min, current_session):
      years_list.append((i, str(i) + '-' + str(i+1)[2:4]))
    session = str(year) + '-' + str(year+1)[2:4]
    cptmembers = CPTMember.objects.filter(year = year).order_by('name')
    # A tuple of member, companies map
    details = []
    for member in cptmembers :
      details.append((member, Company.objects.filter(contact_person = member)))
    if year == current_session :
      members_editable = True
    else :
      members_editable = False
    return render_to_response('placement/cpt_list.html', {
        'details' : details,
        'session' : session,
        'current_year' : current_session,
        'year_displaying' : year,
        'years_list' : years_list,
        'members_editable' : members_editable
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to view cpt member list.')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def cpt_add(request) :
  """
  Add a CPT member
  """
  try :
    l.info (request.user.username + ': adding CPT member')
    if request.method == 'POST' :
      form = BaseModelFormFunction(CPTMember, exclude_list=('year', ), data = request.POST)
      if form.is_valid() :
        instance = form.save(commit = False)
        instance.year = current_session_year()
        instance.save()
        l.info(request.user.username + ': added '+ instance.name + 'as a CPT member')
        messages.success(request, 'Successfully added ' + instance.name + ' as a CPT member.')
        return HttpResponseRedirect(reverse('placement.views_admin.cpt'))
    else :
      form = BaseModelFormFunction(CPTMember, exclude_list=('year', ))
    return render_to_response('placement/basic_form.html', {
        'form' : form,
        'title' : 'CPT Member'
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to adding CPT member')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def cpt_edit(request, member_id) :
  """
  Edit a CPT member
  """
  try :
    l.info(request.user.username + ': editing CPT member with ID ' + member_id)
    member = get_object_or_404(CPTMember, pk = member_id,year = current_session_year())
    if request.method == 'POST' :
      form = BaseModelFormFunction(CPTMember,exclude_list = ('year', ), data = request.POST, instance = member)
      if form.is_valid() :
        form.save()
        l.info(request.user.username + ': Updated the information of CPT member ' + member.name + '.')
        messages.success(request, 'Updated the information of CPT member ' + member.name + '.')
        return HttpResponseRedirect(reverse('placement.views_admin.cpt'))
    else :
      form = BaseModelFormFunction(CPTMember, exclude_list = ('year', ), instance = member)
    return render_to_response('placement/basic_form.html', {
        'form' : form
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to editing CPT member')
    l.exception(e)
    return handle_exc(e, request)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def cpt_delete(request, member_id) :
  """
  Delete a CPT member
  """
  try :
    Company.objects.filter(contact_person = member_id).update(contact_person = None)
    member = CPTMember.objects.get(pk = member_id)
    member.delete()
    l.info(request.user.username + ': Deleted CPT member ' + member.name + '.')
    messages.success(request, 'Deleted ' + member.name + ' from the list of CPT members.')
    return HttpResponseRedirect(reverse('placement.views_admin.cpt'))
  except Exception as e :
    l.info(request.user.username + ': encountered exception when trying to delete CPT member')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin')).exists(), login_url=login_url)
def notices(request, page_no = None) :
  """
  Display a list of all the forms available. It supports paging.
  """
  l.info(request.user.username + ': viewing notices')
  try :
    if not page_no :
      page_no = 1
    else :
      page_no = int(page_no)
    notices = Notices.objects.all().order_by('-date_of_upload')
    pages = range(1,(notices.count()+19)/10)
    # Do not display paging if there is only a single page
    if len(pages) == 1 :
      pages = None
    notices = notices[(page_no-1)*10:page_no*10]
    return render_to_response('placement/notices_list.html', {
        'notices' : notices,
        'pages' : pages,
        'page_no' : page_no
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to view notices')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def notice_upload(request) :
  """
  Upload a Notice.
  """
  try :
    l.info(request.user.username + ': Uploading Notices')
    if request.method == 'POST' :
      form = forms.NoticesForm(request.POST, request.FILES)
      if form.is_valid() :
        form.save()
        l.info(request.user.username + ': Notice uploaded successfully.')
        messages.success(request, 'The notice was uploaded successfully.')
        return HttpResponseRedirect(reverse('placement.views_admin.notices'))
    else :
      form = forms.NoticesForm()
    return render_to_response('placement/basic_form.html', {
        'form' : form,
        'title' : 'Upload a form',
        'action' : reverse('placement.views_admin.notice_upload')
        }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when trying to upload a notice')
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
      return render_to_response('placement/branch_details_list.html', {
          'branches' : Branch.objects.all().order_by('department'),
          }, context_instance = RequestContext(request))
    # Display list of students in the specified branch
    branch = get_object_or_404(Branch, code = branch_code)
    l.info(request.user.username + ': Viewing Students of ' + branch.name)
    plac_persons = PlacementPerson.objects.filter(person__branch = branch, status = 'VRF', person__passout_year = None).order_by('person__name')
    details = []
    # TODO : Put all these queries into one per model
    educational_details = EducationalDetails.objects.all()
    person_info_all = StudentInfo.objects.all()
    apps = CompanyApplicationMap.objects.all()
    for plac_person in plac_persons :
      student = plac_person.student
      try :
        #tenth_marks = EducationalDetails.objects.get(student = student, course = '10TH').cgpa
        tenth_marks = educational_details.get(student = student, course = '10TH').cgpa
      except EducationalDetails.DoesNotExist :
        tenth_marks = '-'
      try :
        #twelfth_marks = EducationalDetails.objects.get(student = student, course = '12TH').cgpa
        twelfth_marks = educational_details.get(student = student, course = '12TH').cgpa
      except EducationalDetails.DoesNotExist :
        twelfth_marks = '-'
      #graduation_marks = EducationalDetails.objects.get(student = student, course = 'UG0').cgpa
      graduation_marks = educational_details.filter(student = student, course = 'UG0')
      if graduation_marks:
        graduation_marks = graduation_marks[0].cgpa
      else:
        graduation_marks = '-'
      try :
        #person_info = StudentInfo.objects.get(student = student)
        person_info = person_info_all.get(student =student)
      except StudentInfo.DoesNotExist :
        person_info = None
      #applications = CompanyApplicationMap.objects.filter(plac_person = plac_person)
      applications = apps.filter(plac_person = plac_person)
      if applications:
        no_of_applications = applications.count()
        last_application = applications.order_by('-time_of_application')[0].time_of_application
      else :
        no_of_applications = 0
        last_application = "-"
      details.append((plac_person,tenth_marks,twelfth_marks,graduation_marks, person_info, no_of_applications, last_application))
    return render_to_response('placement/branch_details.html', {
          'branch' : branch,
          'details' : details
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when viewing branch details')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def second_round(request) :
  """
  Stores whether a branch is open for second round or not.
  It hanldes the save/show uses.
  """
  try :
    l.info(request.user.username + ': Going into branch list for Second Round')
    year = current_session_year()
    if request.method == 'POST' :
      # TODO : you may want to use a transaction
      SecondRound.objects.filter( year = year ).delete()
      for pk in request.POST.getlist('branches_for_second_round') :
        SecondRound.objects.create( year = year,
                                    branch = Branch.objects.get( pk = pk )
                                    )
      l.info(request.user.username + ': Updated the Second Round information.')
      messages.success(request, 'Updated the Second Round information.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    else :
      return render_to_response('placement/second_round.html', {
          'branches' : Branch.objects.all(),
          'second_round_branches' : SecondRound.objects.filter( year = current_session_year() ).values_list('branch__pk', flat=True)
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': encountered exception when viewing second round')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def downloads(request) :
  """
  Show a html page to download various statistics in XLS format
  to admin
  """
  l.info(request.user.username + ': viewing downloads')
  return render_to_response('placement/admin/downloads.html',
                            context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def branch_details_xls(request, branch_code) :
  """
  Display list of students in a branch. If no branch is specified, it displays
  list of all the branches.
  """
  try :
    # Display xls list of students in the specified branch
    branch = get_object_or_404(Branch, code = branch_code)
    l.info(request.user.username + ': Viewing xls list of Students of ' + branch.name)
    plac_persons = PlacementPerson.objects.filter(person__branch = branch, status = 'VRF', person__passout_year = None).order_by('person__name')
    details = []
    # TODO : Put all these queries into one per model
    educational_details = EducationalDetails.objects.all()
    person_info_all = StudentInfo.objects.all()
    apps = CompanyApplicationMap.objects.all()
    for plac_person in plac_persons:
      student = plac_person.student
      try :
        #tenth_marks = EducationalDetails.objects.get(student = student, course = '10TH').cgpa
        tenth_marks = educational_details.get(student = student, course = '10TH').cgpa
      except EducationalDetails.DoesNotExist :
        tenth_marks = '-'
      try :
        #twelfth_marks = EducationalDetails.objects.get(student = student, course = '12TH').cgpa
        twelfth_marks = educational_details.get(student = student, course = '12TH').cgpa
      except EducationalDetails.DoesNotExist :
        twelfth_marks = '-'
      #graduation_marks = EducationalDetails.objects.get(student = student, course = 'UG0').cgpa
      graduation_marks = educational_details.filter(student = student, course = 'UG0')
      if graduation_marks:
        graduation_marks = graduation_marks[0].cgpa
      else:
        graduation_marks = '-'
      try :
        #person_info = StudentInfo.objects.get(student = student)
        person_info = person_info_all.get(student =student)
      except StudentInfo.DoesNotExist :
        person_info = None
      #applications = CompanyApplicationMap.objects.filter(plac_person = plac_person)
      applications = apps.filter(plac_person = plac_person)
      details.append((plac_person,tenth_marks,twelfth_marks,graduation_marks, person_info))
    wbk = xlwt.Workbook()
    heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
    sheet = wbk.add_sheet('Verified students')
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 11, 'Students verified for \'' + branch.name + '\' as on ' + datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p'), heading_xf)
    headers = ('S.No.', 'Enrollment No', 'Name', 'CGPA', 'Birth Date', 'Tenth Marks', 'Twelfth Marks', 'Graduation Marks', 'Category', 'Email ID', 'Contact No', 'Course')
    for (col, heading) in enumerate(headers) :
      sheet.write(2, col, heading, heading_xf)
    row = 3
    for detail in details:
      sheet.write(row, 0, row - 2)
      sheet.write(row, 1, detail[0].student.user.username)
      sheet.write(row, 2, detail[0].student.name)
      sheet.write(row, 3, detail[0].student.cgpa)
      sheet.write(row, 4, detail[4].birth_date.strftime('%b. %d, %Y'))
      sheet.write(row, 5, detail[1])
      sheet.write(row, 6, detail[2])
      sheet.write(row, 7, detail[3])
      sheet.write(row, 8, detail[4].get_category_display())
      sheet.write(row, 9, detail[0].student.email_id)
      sheet.write(row, 10, detail[0].student.personal_contact_no)
      sheet.write(row, 11, detail[0].student.get_semester_display())
      row += 1
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + sanitise_for_download(branch.name) + '_Verified.xls'
    wbk.save(response)
    return response
  except Exception as e:
    l.info(request.user.username + ': encountered exception when viewing branch details')
    l.exception(e)
    return handle_exc(e, request)

@csrf_exempt
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def insert_shortlist(request):
  if request.method == 'POST':
    students = request.POST['students'].strip().split(",")
    company_id = request.POST['company'].strip()
    message = ""
    is_success = True
    try:
      company = Company.objects.get(pk = int(company_id))
      for student in students:
        student = Student.objects.get(user__username=int(student))
        plac_person = PlacementPerson.objects.get_or_create(student=student)[0]
        c_map,created = CompanyApplicationMap.objects.get_or_create(plac_person=plac_person,company=company)
        if created:
          c_map.status = 'FIN'
        c_map.shortlisted = True
        c_map.save()
    except Company.DoesNotExist:
      message = "Given Company does not exist. Please try again."
      is_success = False
    except Student.DoesNotExist:
      message= "Given enrollment Number/Numbers are not correct. Please try again"
      is_success = False
    except Exception as e:
        message = "Some error occured. Please contact IMG"
        is_success = False
    if not message:
      message = "Saved Successfully"
    json_data = json.dumps({'message':message,'is_success':is_success})
    return HttpResponse(json_data,content_type='application/json')
  form = forms.AddShortlistForm()
  return render_to_response('placement/admin/shortlist.html',{
                            'form':form,},
                            context_instance = RequestContext(request))
