from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Min, Count
from django.contrib import messages

import logging
import os, xlwt, datetime
import mimetypes

from nucleus.models import User, Student, WebmailAccount, Branch
# import models  #from placement
from placement.utils import handle_exc, get_ctc, sanitise_for_download
from placement.policy import current_session_year
from placement import constants as PC
from placement.models import *
from api import model_constants as MC
from collections import defaultdict

from django.conf import settings

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

# XXX : Keep logged after all imports only
# As other imports might over write the logger
l = logging.getLogger('placement')

@login_required
def photo(request) :
  """
    Returns the photo of plac_person. Gives default photo incase it doesnt exist.
  """
  #Not logging this function as it is going to be called in each view.
  try :
    photo = request.user.student.placementperson.photo
  except Exception as e :
    photo = None
  if photo and os.path.exists(photo.path) :
    filename = photo.path
  else :
    # give a default image if not image is uploaded. Make sure that this file exists.
    filename = settings.MEDIA_ROOT + 'placement/photos/default.jpg'
  wrapper = FileWrapper(file(filename))
  response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
  response['Content-Length'] = os.path.getsize(filename)
  return response

@login_required
def brochures(request, company_id) :
  """
    Returns the brochure of a particular company
  """
  try :
    l.info(request.user.username+': Downloading Brochure for '+str(company_id))
    brochure = get_object_or_404(models.Company,id = company_id).brochure
    if brochure :
      filename = brochure.path
    else :
      raise Http404
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
    response['Content-Length'] = os.path.getsize(filename)
    return response
  except Exception as e :
    l.info(request.user.username+': Encountered Exception while Downloading Brochure for '+str(company_id))
    l.exception(e)
    messages.error(request, 'An error occured while fetching the brochure.')
    return handle_exc(e, request)

@login_required
def submitted_resume(request, company_id) :
  """
  Returns the resume submitted by the user to specific company.
  """
  try :
    l.info(request.user.username+': Downloading Resumes for '+str(company_id))
    student = request.user.student
    filename = os.path.join(settings.MEDIA_ROOT, 'placement', 'applications', 'company'+str(company_id), str(student.user.username)+'.pdf')
    if not os.path.exists(filename) : # the user has not applied to the company
      raise Http404
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type=mimetypes.guess_type(filename)[0])
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename=Resume.pdf'
    return response
  except Exception as e :
    l.info(request.user.username+': Encountered Exception while downloading submitted resumes for '+str(company_id))
    l.exception(e)
    messages.error(request, 'An error occured while generating the pdf file.')
    return handle_exc(e, request)


# TODO : Make sure that each query in this view checks for year
# TODO : Test the XLS file with original data
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def institute_results_sectorwise(request) :
  """
  Generates a XLS file for institute results.
  The XLS file has multiple tabs/sheets in it :
    1. graduations by sectors - no of companies arrived
    2. graduations by sectors - no placed students
    3. branch by sectors  - no of companies arrived
    4. branch by sectors  - no placed students
      two tabs each for no of companies arrived and no of placed students for each graduation by all sectors
      e.g. ug_branches by sectors = 2 tabs
  """
  l.info(request.user.username+': viewing institute resuts sectorwise')
  current_session = current_session_year()
  response = HttpResponse(content_type='application/ms-excel')
  time = datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p')
  response['Content-Disposition'] = 'attachment; filename=institute_results_sectorwise_' + sanitise_for_download(time) + '.xls'
  wbk = xlwt.Workbook()
  heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
  # List of branches, graduations and sectors for inserting cells in the XLS
  # sheet in that order
  list_sector = zip(*PC.COMPANY_RESUME_CHOICES)[0]
  list_graduation = zip(*MC.GRADUATION_CHOICES)[0]
  list_branch = {}
  list_branch['overall'] = list(Branch.objects.values_list('code', flat=True))
  for graduation in list_graduation :
    list_branch[graduation] = list(Branch.objects.filter(graduation = graduation).values_list('code', flat=True))
  branch_graduation_dict = {}
  for branch in Branch.objects.all() :
    branch_graduation_dict[branch.code] = branch.graduation
  # Sectorwise - Companies Arrived
  # TOVERIFY : What if a student is placed in two companies?
  # Currently showing it in both the categories
  sheet = wbk.add_sheet('Sectorwise - Companies Arrived')
  sheet.set_panes_frozen(True)
  sheet.set_horz_split_pos(3)
  sheet.set_remove_splits(True)
  sheet.write_merge(0, 1, 0, 6, 'Number of companies arrived for placement as on ' + time, heading_xf)
  sheet.write(2, 1, 'Overall', heading_xf)
  for (col, title) in enumerate(zip(*MC.GRADUATION_CHOICES)[1]) :
    sheet.write(2, col+2, title, heading_xf)
  for (row, (sect_id,sect_name)) in enumerate(PC.COMPANY_RESUME_CHOICES) :
    sheet.write(row+3, 0, sect_name, heading_xf)
  for company in Company.objects.filter(year__exact = current_session).values('sector').annotate(count = Count('sector')) :
    sheet.write(list_sector.index(company['sector'])+3, 1, company['count'])
  counts = {} # Dictionary to store the no. of companies open for a graduation
  for company in list(Company.objects.filter(year__exact = current_session).values('name', 'sector','open_for_disciplines__graduation').distinct()) :
    try :
      old_dict = counts[company['sector']]
    except KeyError as k :
      counts[company['sector']] = {}
    try :
      old_value = counts[company['sector']][company['open_for_disciplines__graduation']]
    except KeyError as k :
      counts[company['sector']][company['open_for_disciplines__graduation']] = 0
    counts[company['sector']][company['open_for_disciplines__graduation']] += 1
  for sector, graduations_list in counts.items() :
    for graduation, count in graduations_list.items() :
      sheet.write(list_sector.index(sector)+3, list_graduation.index(graduation)+2, count)
  # Sectorwise - Students Placed
  sheet = wbk.add_sheet('Sectorwise - Students Placed')
  sheet.set_panes_frozen(True)
  sheet.set_horz_split_pos(3)
  sheet.set_remove_splits(True)
  sheet.write_merge(0, 1, 0, 6, 'Number of students placed as on ' + time, heading_xf)
  sheet.write(2, 1, 'Overall', heading_xf)
  for (col, title) in enumerate(zip(*MC.GRADUATION_CHOICES)[1]) :
    sheet.write(2, col+2, title, heading_xf)
  for (row, (sect_id,sect_name)) in enumerate(PC.COMPANY_RESUME_CHOICES) :
    sheet.write(row+3, 0, sect_name, heading_xf)
  for result in Results.objects.filter(company__year__exact = current_session).values('company__sector').annotate(count=Count('company__sector')) :
    sheet.write(list_sector.index(result['company__sector'])+3,
                1, result['count'])
  for result in Results.objects.filter(company__year__exact = current_session).values('company__sector','student__branch__graduation').annotate(count=Count('company__sector')) :
    sheet.write(list_sector.index(result['company__sector'])+3,
                list_graduation.index(result['student__branch__graduation'])+2,
                result['count'])
  sheet_bwise_comp_arrived = wbk.add_sheet('Branchwise - Companies Arrived')
  sheet_bwise_stud_placed = wbk.add_sheet('Branchwise - Students Placed')
  # Graduationwise sheets
  sheets_comp_arrived = []
  sheets_stud_placed = []
  for graduation in list_graduation :
    # Add sheets here, but the data is to be added when adding branchwise data
    sheet = wbk.add_sheet(graduation + ' - Companies Arrived')
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 6, 'Number of companies arrived as on ' + time, heading_xf)
    sheet.write(2, 1, 'Overall', heading_xf)
    for (col, title) in enumerate(zip(*PC.COMPANY_RESUME_CHOICES)[1]) :
      sheet.write(2, col+2, title, heading_xf)
    for (row, branch) in enumerate(Branch.objects.filter(graduation = graduation)) :
      sheet.write(row+3, 0, branch.name, heading_xf)
    sheets_comp_arrived.append(sheet)
    sheet = wbk.add_sheet(graduation + ' - Students Placed')
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 6, 'Number of students placed as on ' + time, heading_xf)
    sheet.write(2, 1, 'Overall', heading_xf)
    for (col, title) in enumerate(zip(*PC.COMPANY_RESUME_CHOICES)[1]) :
      sheet.write(2, col+2, title, heading_xf)
    for (row, branch) in enumerate(Branch.objects.filter(graduation = graduation)) :
      sheet.write(row+3, 0, branch.name, heading_xf)
    sheets_stud_placed.append(sheet)
  # Branchwise - Companies Arrived
  sheet = sheet_bwise_comp_arrived
  sheet.set_panes_frozen(True)
  sheet.set_horz_split_pos(3)
  sheet.set_remove_splits(True)
  sheet.write_merge(0, 1, 0, 6, 'Number of companies arrived as on ' + time, heading_xf)
  sheet.write(2, 1, 'Overall', heading_xf)
  for (col, title) in enumerate(zip(*PC.COMPANY_RESUME_CHOICES)[1]) :
    sheet.write(2, col+2, title, heading_xf)
  for (row, branch) in enumerate(Branch.objects.all()) :
    sheet.write(row+3, 0, branch.name, heading_xf)
  for company in Company.objects.filter(year__exact = current_session).values('open_for_disciplines').annotate(count=Count('open_for_disciplines')) :
    sheet.write(list_branch['overall'].index(company['open_for_disciplines'])+3,
                1, company['count'])
    graduation = branch_graduation_dict[company['open_for_disciplines']]
    sheets_comp_arrived[list_graduation.index(graduation)
                        ].write(list_branch[graduation].index(company['open_for_disciplines'])+3,
                                1, company['count'])
  for company in Company.objects.filter(year__exact = current_session).values('open_for_disciplines','sector').annotate(count=Count('open_for_disciplines')) :
    sheet.write(list_branch['overall'].index(company['open_for_disciplines'])+3,
                list_sector.index(company['sector'])+2,
                company['count'])
    graduation = branch_graduation_dict[company['open_for_disciplines']]
    sheets_comp_arrived[list_graduation.index(graduation)
                        ].write(list_branch[graduation].index(company['open_for_disciplines'])+3,
                                list_sector.index(company['sector'])+2,
                                company['count'])
  # Branchwise - Students Placed
  sheet = sheet_bwise_stud_placed
  sheet.set_panes_frozen(True)
  sheet.set_horz_split_pos(3)
  sheet.set_remove_splits(True)
  sheet.write_merge(0, 1, 0, 6, 'Number of students placed as on ' + time, heading_xf)
  sheet.write(2, 1, 'Overall', heading_xf)
  for (col, title) in enumerate(zip(*PC.COMPANY_RESUME_CHOICES)[1]) :
    sheet.write(2, col+2, title, heading_xf)
  for (row, branch) in enumerate(Branch.objects.all()) :
    sheet.write(row+3, 0, branch.name, heading_xf)
  for result in Results.objects.filter(company__year__exact = current_session).values('student__branch').annotate(count=Count('student__branch')) :
    sheet.write(list_branch['overall'].index(result['student__branch'])+3,
                1, result['count'])
    graduation = branch_graduation_dict[result['student__branch']]
    sheets_stud_placed[list_graduation.index(graduation)
                        ].write(list_branch[graduation].index(result['student__branch'])+3,
                                1, result['count'])
  for result in Results.objects.filter(company__year__exact = current_session).values('student__branch','company__sector').annotate(count=Count('student__branch')) :
    sheet.write(list_branch['overall'].index(result['student__branch'])+3,
                list_sector.index(result['company__sector'])+2,
                result['count'])
    graduation = branch_graduation_dict[result['student__branch']]
    sheets_stud_placed[list_graduation.index(graduation)
                        ].write(list_branch[graduation].index(result['student__branch'])+3,
                                list_sector.index(result['company__sector'])+2,
                                result['count'])
  wbk.save(response)
  return response

# TODO : Make sure that each query in this view checks for year
# TODO : Test the XLS file with original data
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def institute_results_companywise(request) :
  """
  Render statistics of all the company in various graduations
  """
  l.info(request.user.username+': getting institute results companywise')
  current_session = current_session_year()
  response = HttpResponse(content_type='application/ms-excel')
  time = datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p')
  response['Content-Disposition'] = 'attachment; filename=institute_results_companywise_' + sanitise_for_download(time) + '.xls'
  wbk = xlwt.Workbook()
  heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
  sheet = wbk.add_sheet('Placements - Companywise')
  sheet.set_panes_frozen(True)
  sheet.set_horz_split_pos(3)
  sheet.set_remove_splits(True)
  sheet.write_merge(0, 1, 0, 6, 'Number of students placed in companies as on ' + time, heading_xf)
  sheet.write(2, 1, 'Sector', heading_xf)
  sheet.write(2, 2, 'Total', heading_xf)
  sheet.write(2, 6, 'Average CTC', heading_xf)
  graduation_col_map = {}
  for (col, (id, title)) in enumerate(MC.GRADUATION_CHOICES) :
    sheet.write(2, col+3, title, heading_xf)
    graduation_col_map[id] = col
  company_row_map = {}
  last_row = defaultdict(int)
  row = 0
  last_row['overall']=0
  for row, result in enumerate(Results.objects.filter(company__year__exact = current_session).values('company','company__name').annotate(count = Count('company')).order_by('company__name')) :
    company = Company.objects.get(id = result['company'])
    sheet.write(row+3, 0, company.name, heading_xf)
    sheet.write(row+3, 1, company.sector)
    sheet.write(row+3, 2, result['count'])
    last_row['overall'] += result['count']
    company_row_map[result['company']] = row
  last_row_num = row + 1

  total_ctc = defaultdict(int)
  total_selections = defaultdict(int)
  for result in Results.objects.filter(company__year__exact = current_session).values('company', 'student__branch__graduation').annotate(count = Count('company')) :
    grad = result['student__branch__graduation']
    row = company_row_map[result['company']] + 3
    sheet.write(row, graduation_col_map[grad]+3, result['count'])
    company = Company.objects.get(id = result['company'])
    package = company.__getattribute__('package_' + grad.lower())  # it's a hack
    total_ctc[row] += get_ctc(package)
    total_selections[row] += result['count']
    last_row[result['student__branch__graduation']] += result['count']

  sheet.write(last_row_num+3, 2, last_row.pop('overall'), heading_xf)
  for graduation, count in last_row.items() :
    sheet.write(last_row_num+3, graduation_col_map[graduation]+3, count, heading_xf)
  for row, ctc in total_ctc.items() :
    if not total_selections[row] :
      total_selections[row] = 1
    sheet.write(row, 6, ctc/total_selections[row])
  wbk.save(response)
  return response

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def institute_results_branchwise(request) :
  """
  Render statistics of all the branches
  """
  l.info(request.user.username+': getting institute results branchwise')
  current_session = current_session_year()
  response = HttpResponse(content_type='application/ms-excel')
  time = datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p')
  response['Content-Disposition'] = 'attachment; filename=institute_results_branchwise_' + sanitise_for_download(time) + '.xls'
  wbk = xlwt.Workbook()
  heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')

  # Branches which have atleast a single student placed
  branches = Results.objects.filter(company__year__exact = current_session).values_list('student__branch', flat = True).distinct()
  for branch in branches :
    branch = Branch.objects.get(code = branch)
    sheet = wbk.add_sheet(branch.department + '-' + branch.code)
    sheet.set_panes_frozen(True)
    sheet.set_horz_split_pos(3)
    sheet.set_remove_splits(True)
    sheet.write_merge(0, 1, 0, 6, 'Number of students placed in ' + branch.name + ' as on ' + time, heading_xf)
    sheet.write(2, 0, 'Name', heading_xf)
    sheet.write(2, 1, 'CGPA', heading_xf)
    sheet.write(2, 2, 'Company 1', heading_xf)
    sheet.write(2, 3, 'CTC 1', heading_xf)
    sheet.write(2, 4, 'Company 2', heading_xf)
    sheet.write(2, 5, 'CTC 2', heading_xf)
    total_ctc = 0
    total_placed = 0
    # students which are placed in at least 1 company
    students = Results.objects.filter(company__year__exact = current_session, student__branch = branch).order_by('-student__cgpa').values_list('student', flat = True).distinct()
    for row, student in enumerate(students) :
      # The student may get placed in two companies as well
      placements = Results.objects.filter(company__year__exact = current_session, student = student)
      student = placements[0].student # convert the id of student into full student
      sheet.write(row+3, 0, student.name, heading_xf)
      sheet.write(row+3, 1, student.cgpa)
      company1 = placements[0].company
      sheet.write(row+3, 2, company1.name)
      # whether student is ug/pg/phd
      grad = student.branch.graduation.lower()
      sheet.write(row+3, 3, company1.__getattribute__('package_' + grad))
      ctc1 = get_ctc(company1.__getattribute__('package_' + grad))
      ctc2 = 0
      total_placed += 1
      if placements.count() == 2 :
        company2 = placements[1].company
        sheet.write(row+3, 4, company2.name)
        sheet.write(row+3, 5, company2.__getattribute__('package_' + grad))
        ctc2 = get_ctc(company2.__getattribute__('package_' + grad))
      elif placements.count() > 2 :
        # TODO : Handle this error!!!
        pass
      if ctc2 > ctc1 :
        total_ctc += ctc2
      else :
        total_ctc += ctc1
    sheet.write(row+5, 1, 'Average CTC', heading_xf)
    sheet.write(row+5, 2, total_ctc/total_placed, heading_xf)
  wbk.save(response)
  return response

def institute_results(request) :
  """
  Download XLS list of all the placed students
  """
  # This view is optimized for best performance
  # using foreign key reference fires a db query, so don't use them
  current_session = current_session_year()
  results = Results.objects.filter(company__year__exact = current_session
                                   ).values_list('student', 'company')
  results_map = {}
  companies = set()
  for (student, company) in results :
    if student in results_map.keys() :
      results_map[student].append(company)
    else :
      results_map[student] = [company]
    companies.add(company)
  students_map = {}
  users = []
  for student in Student.objects.filter(pk__in = results_map.keys()) :

    students_map[student.pk] = {'name' : student.name,
                              'cgpa' : student.cgpa,
                              'branch' : student.branch.name,
                              'year' : 1 + current_session - int(student.admission_year),
                              'email_id' : student.user.email,
                              'contact_no' : student.user.contact_no,
                              }
    users.append(student.user_id)
  companies_map = {}
  for company in Company.objects.filter(pk__in = companies) :
    companies_map[company.pk] = company.name
  users_map = {}
  for user in User.objects.filter(id__in = users) :
    users_map[user.pk] = user.username
  branch_map = {}
  for branch in Branch.objects.all() :
    branch_map[branch.pk] = {'name' : branch.name, 'degree' : branch.degree}
  wbk = xlwt.Workbook()
  heading_xf = xlwt.easyxf('font: bold on; align: vert centre, horiz center')
  sheet = wbk.add_sheet('Finalized students')
  sheet.set_panes_frozen(True)
  sheet.set_horz_split_pos(3)
  sheet.set_remove_splits(True)
  sheet.write_merge(0, 1, 0, 9, 'Students placed as on '
                    + datetime.datetime.now().strftime('%b. %d, %Y, %I:%M %p'), heading_xf)
  headers = ('S.No.', 'Enrollment No', 'Name', 'Course', 'Discipline',
             'CGPA', 'Company1', 'Company2', 'Contact No', 'Email ID')
  for (col, heading) in enumerate(headers) :
    sheet.write(2, col, heading, heading_xf)
  for (row, student_id) in enumerate(results_map) :
    row += 3
    student_detail = students_map[student_id]
    branch_detail = branch_map[student_detail['branch']]
    result_detail = results_map[student_id]
    sheet.write(row, 0, row-2)
    sheet.write(row, 1, users_map[student_id])
    sheet.write(row, 2, student_detail['name'])
    sheet.write(row, 3, branch_detail['name'])
    sheet.write(row, 4, branch_detail['degree'])
    sheet.write(row, 5, student_detail['cgpa'])
    sheet.write(row, 6, companies_map[result_detail[0]])
    if len(result_detail) > 1 :
      sheet.write(row, 7, companies_map[result_detail[1]])
    sheet.write(row, 8, student_detail['contact_no'])
    sheet.write(row, 9, student_detail['email_id'])
  response = HttpResponse(content_type='application/ms-excel')
  response['Content-Disposition'] = 'attachment; filename=' + sanitise_for_download(company.name) + '_Applications.xls'
  wbk.save(response)
  return response
