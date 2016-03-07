from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages

import logging
import xlwt, datetime

from nucleus.models import Student, Branch
from placement import forms
from placement.policy import current_session_year
from placement.models import *
from placement.utils import *

l = logging.getLogger('placement')

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# IMPORTANT : Objects of Student and PlacementPerson are to be stored in session.
# These objects are used in all the templates.

# Placement verification views start
# TODO : Make sure that these views have used user_passes_test decorator
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def index(request) :
  """
  Index page for Placement Verification.
  """
  l.info(request.user.username + ': In index page for verification')
  try:
    results = None
    if request.method == 'POST' :
      # Show search results
      form = forms.VerifySearch(request.POST)
      if form.is_valid() :
        search_string = form.cleaned_data['search_string']
        results = PlacementPerson.objects.filter(student__passout_year = None).only('student')
        if search_string.isdigit() :
          results = results.filter(student__user__username__icontains = search_string).order_by('student__user__username')
        else :
          results = results.filter(student__user__name__icontains = search_string, status__in = ('VRF', 'OPN', 'LCK')).order_by('student__user__name')
    elif request.GET.has_key('debar') :
      form = forms.VerifySearch()
      results = PlacementPerson.objects.filter(student__passout_year=None, is_debarred=True).only('student').order_by('student__user__username')
    else :
      form = forms.VerifySearch()
    return render_to_response('placement/verify_index.html', {
        'form' : form,
        'submit' : 'Search',
        'results' : results
        },
        context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while in index for verify')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def branch_list(request) :
  """
  Display a list of branches to the user Verify, from where he can opt to verify/unverify/unlock/reverify
  students of a branch.
  """
  try :
    l.info(request.user.username + ': viewing branch list for verification')
    return render_to_response('placement/verify_branch_list.html', {
        'branches' : Branch.objects.all().order_by('department'),
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing branch list ()')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def unverified_list(request) :
  """
  Returns a XLS file containing the list of unverified students.
  """
  try :
    l.info(request.user.username + ': downloading xls list for unverified students')
    plac_persons = PlacementPerson.objects.filter(status__in = ('LCK', ))
    response = HttpResponse(content_type='application/ms-excel')
    # TODO : Format the date and time properly and set the file size in the response
    response['Content-Disposition'] = ('attachment; filename=UnverifiedStudents_' +
                                       sanitise_for_download(datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p')) + '.xls')
    wbk = xlwt.Workbook()
    heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
    sheet = wbk.add_sheet('Unverified students')
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 4, 'List of unverified students as on ' + datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p'), heading_xf)
    headers = ('S.No.', 'Enrollment No.', 'Name', 'Discipline', 'Course')
    for (col, heading) in enumerate(headers) :
      sheet.write(2, col, heading, heading_xf)
    for (row, plac_person) in enumerate(plac_persons) :
      student = plac_person.student
      row += 3
      sheet.write(row, 0, row-2)
      sheet.write(row, 1, student.user.username)
      sheet.write(row, 2, student.user.name)
      sheet.write(row, 3, student.branch.name)
      sheet.write(row, 4, student.get_semester_display())
    wbk.save(response)
    return response
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing branch list ()')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def verify(request, task, branch_code) :
  """
  Verify/Unverify/Unlock/Reverify students of a branch enrolled in a particular degree.
  It displays the list of verified students also.
  """
  try :
    l.info(request.user.username + ': (un/re)verify/unlock students ' + branch_code + " " + task)
    if task == 'verify' :
      from_status = 'LCK'
      to_status = 'VRF'
    elif task == 'unverify' :
      from_status = 'VRF'
      to_status = 'LCK'
    elif task == 'unlock' :
      from_status = 'VRF'
      to_status = 'OPN'
    elif task == 'reverify' :
      from_status = 'OPN'
      to_status = 'VRF'
    elif task == 'verified' :
      from_status = 'VRF'
    if request.method == 'POST' :
      selected_students = request.POST.getlist('selected_students')
      PlacementPerson.objects.filter(pk__in = selected_students).update(status = to_status)
      logging_list = PlacementPerson.objects.filter(pk__in = selected_students).values_list('student__user__username')
      l.info(request.user.username + ': updated the status of the following from '+str(from_status)+' to '+str(to_status)+'-- '+str(logging_list))
      messages.success(request, 'Your action was completed successfully.')
      return HttpResponseRedirect(reverse('placement.views_verify.verify',kwargs={'task': task, 'branch_code': branch_code}))
    else :
      # TOVERIFY : Is it required to display birth date and userid in this view?
      # TODO : If yes, display them as well
      branch = Branch.objects.get(code = branch_code)
      plac_persons = PlacementPerson.objects.filter(status = from_status,
                                                student__branch = branch,
                                                student__passout_year = None
                                                ).only('student', 'id').order_by('student__user__name')
      return render_to_response('placement/verify_list.html', {
          'plac_persons' : plac_persons,
          'branch' : branch,
          'task' : task
          }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while (re/un)verifying/unlocking ' + branch_code + " " + task)
    l.exception(e)
    return handle_exc(e, request)

# TODO : Make sure that this view is available only to the user Verify.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def resume(request, enrollment_no) :
  """
  Shows the resume of a student to the user Verify.
  """
  try :
    l.info(request.user.username + ': resume student ' + enrollment_no)
    student = Student.objects.get(user__username=enrollment_no)
    pdf = get_resume_binary(RequestContext(request), student, 'VER', verification_resume = True)
    if pdf['err'] :
      messages.error(request, 'An error occured while generating the PDF file.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Resume_' + enrollment_no + '.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e :
    l.info(request.user.username + ': encountered exception while showing resume of student to user verify')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def scorecard(request, enrollment_no) :
  """
  Shows the scorecard of a student to the user Verify.
  """
  try :
    l.info(request.user.username + ': scorecard for student ' + enrollment_no)
    student = Student.objects.get(user__username=enrollment_no)
    pdf = get_scorecard_binary(RequestContext(request), student)
    if pdf['err'] :
      messages.error(request, 'An error occured while generating the PDF file.')
      return HttpResponseRedirect(reverse('placement.views.index'))
    response = HttpResponse(pdf['content'], content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Scorecard_' + enrollment_no + '.pdf'
    response['Content-Length'] = len(pdf['content'])
    return response
  except Exception as e :
    l.info(request.user.username + ': encountered exception while showing scorecard of student to user verify')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def department_list(request) :
  """
  Display a list of departments to the user Verify, from where he can opt to verify/unverify/unlock/reverify
  students of a department.
  """
  try :
    l.info(request.user.username + ': viewing department list for verification')
    return render_to_response('placement/verify_department_list.html', {
        'departments' : MC.DEPARTMENT_CHOICES,
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing branch list ()')
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def verify_department(request, task, department_code) :
  """
  Verify/Unverify/Unlock/Reverify students of a dept enrolled in a particular degree.
  It displays the list of verified students also.
  """
  try :
    l.info(request.user.username + ': (un/re)verify/unlock students ' + str(department_code) + " " + str(task))
    if task == 'verify' :
      from_status = 'LCK'
      to_status = 'VRF'
    elif task == 'unverify' :
      from_status = 'VRF'
      to_status = 'LCK'
    elif task == 'unlock' :
      from_status = 'VRF'
      to_status = 'OPN'
    elif task == 'reverify' :
      from_status = 'OPN'
      to_status = 'VRF'
    elif task == 'verified' :
      from_status = 'VRF'
    if request.method == 'POST' :
      PlacementPerson.objects.filter(pk__in = request.POST.getlist('selected_students')).update(status = to_status)
      messages.success(request, 'Your action was completed successfully.')
      return HttpResponseRedirect(reverse('placement.views_verify.verify_department',kwargs={'task': task, 'department_code': department_code}))
    else :
      # TOVERIFY : Is it required to display birth date and userid in this view?
      # TODO : If yes, display them as well
      #branch = Branch.objects.get(department = department_code)
      dept_name = [ name for id, name in MC.DEPARTMENT_CHOICES if id == department_code ][0]
      plac_persons = PlacementPerson.objects.filter(status = from_status,
                                                student__branch__department = dept_name,
                                                student__passout_year = None,
                                                ).only('student', 'id').order_by('student__user__name')
      return render_to_response('placement/verify_list.html', {
          'plac_persons' : plac_persons,
          'department' : dept_name,
          'id' : department_code,
          'task' : task
          }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while (re/un)verifying/unlocking ' + department_code + " " + task)
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def change_status(request, enrollment_no, status = False) :
  """
  Cycles the status of placement person between
  OPN -> LCK ->  VRF -> OPN
  It is to be used via ajax.
  Returns New status on success and 'ERROR : <error message>' on error.
  """
  l.info(request.user.username + ': trying to cycle the placement status of ' + enrollment_no)
  if status <> False and status not in PC.PLACEMENT_STATUS_CHOICES :
    next_status = {'CLS':status, 'OPN':status, 'LCK':status, 'VRF':status}
  else :
    next_status = {'OPN':'LCK', 'LCK':'VRF', 'VRF':'OPN'}
  try :
    plac_person = PlacementPerson.objects.get(student__user__username = enrollment_no)
  except PlacementPerson.DoesNotExist :
    l.info(request.user.username + ': could not find ' + enrollment_no + ' to cycle the placement status.')
    return HttpResponse ('ERROR : Student not found with this enrollment no.')
  try :
    plac_person.status = next_status[plac_person.status]
    plac_person.save()
    l.info(request.user.username + ': cycled placement status of ' + enrollment_no + ' to ' + plac_person.status)
    if status <> False:
      return HttpResponse()
    else :
      return HttpResponse(plac_person.get_status_display())
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while cycling the placement status of ' + enrollment_no)
    l.exception(e)
    return HttpResponse('ERROR : An unknown error occured.')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Verify').exists(), login_url=login_url)
def change_debar_status(request, enrollment_no, status) :
  """
  Changes debarred status of students
  """
  try:
    l.info(request.user.username + ': trying to change debar status of ' + str(enrollment_no) + ' to '+str(status))
    if status == 'Y':
      is_debarred = True
    elif status == 'N':
      is_debarred = False
    else :
      return HttpResponse ('ERROR: Debar status not defined')
    try:
      plac_person = PlacementPerson.objects.get(student__user__username=enrollment_no)
      plac_person.is_debarred = is_debarred
      plac_person.save()
      return HttpResponse()
    except PlacementPerson.DoesNotExist:
      l.info(request.user.username + ': could not find ' + enrollment_no + ' to cycle the debar status.')
      return HttpResponse ('ERROR : Student not found with this enrollment no.')
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while cycling the placement status of ' + enrollment_no)
    l.exception(e)
    return HttpResponse('ERROR : An unknown error occured.')
