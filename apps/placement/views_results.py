from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Min, Count, Q
from django.views.generic.base import TemplateView

import logging, json

from django.contrib import messages

from api import model_constants as MC
from nucleus.models import Branch
from placement import policy
from placement.policy import current_session_year
from placement.models import *
from placement.utils import *

# Permission denied page. User will be redirected to this page if he fails the user_passes_test.
login_url = '/placement/'

l = logging.getLogger('placement')

# IMPORTANT : Objects of Student and PlacementPerson are to be stored in session.
# These objects are used in all the templates.

#Results to be shown to Faculty as well. Hence, the user_passes_test has been commented out.

@login_required
#@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin', 'Placement Department')).exists(), login_url=login_url)
def company_list(request, year = None) :
  """
  View list of companies for the purpose of getting the results for
  a particular year.
  """
  try :
    l.info(request.user.username + ': Viewing company list for results')
    current_session = current_session_year()
    if not year :
      year = current_session
    else :
      year = int(year) # unicode is given by the link
    # Show those companies only which have declared results i.e. have selected at least one student.
    results = Results.objects.filter(company__year__exact = year)
    total_placements = results.count()
    # TODO : check if this query is correct or not!!
    results = results.values_list('company__name', 'company').annotate(placed_count = Count('company')).order_by('company__name')
    # get the year of the oldest result
    year_min = Results.objects.aggregate(min = Min('company__year'))['min']
    if not year_min :
      year_min = current_session
    sessions = []
    for i in range(year_min, current_session):
      sessions.append(str(i) + '-' + str(i+1)[2:4])
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = zip(range(year_min, current_session), sessions)
    session = str(year) + '-' + str(year+1)[2:4]
    return render_to_response('placement/results_company_list.html', {
        'years_list' : years_list,
        'session' : session,
        'year' : year,
        'current_year' : current_session,
        'total_placements' : total_placements,
        'list' : results
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing list of results')
    l.exception(e)
    return handle_exc(e, request)

@login_required
#@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin', 'Placement Department')).exists(), login_url=login_url)
def discipline_list(request, year = None) :
  """
  View list of disciplines for the purpose of getting the results for
  a particular year.
  """
  try :
    l.info(request.user.username + ': Viewing discipline list')
    current_session = current_session_year()
    if not year :
      year = current_session
    else :
      year = int(year) # unicode is given by the link
    # TODO : How to display branches for UG/PG/DUAL etc?
    # Should an option be given to select degree??
    # For the time being, display all the Branch rows.
    results = Results.objects.filter(company__year__exact = year)
    total_placements = results.count()
    branches = results.values_list('student__branch', flat = True).order_by('student__branch').distinct()
    degrees = Branch.objects.filter(pk__in = branches).order_by('name', 'code').values_list('degree')
    results = results.values_list('student__branch__name', 'student__branch').annotate(placed_count = Count('student__branch')).order_by('student__branch__name', 'student__branch__code')
    results = [ (a[0],a[1],a[2],b[0]) for a,b in zip(results,degrees) ]
    # get the year of the oldest company
    year_min = Company.objects.aggregate(min = Min('year'))['min']
    if not year_min :
      year_min = current_session
    sessions = []
    for i in range(year_min, current_session):
      sessions.append(str(i) + '-' + str(i+1)[2:4])
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = zip(range(year_min, current_session), sessions)
    session = str(year) + '-' + str(year+1)[2:4]
    return render_to_response('placement/results_branch_list.html', {
        'years_list' : years_list,
        'session' : session,
        'year' : year,
        'current_year' : current_session,
        'total_placements' : total_placements,
        'list' : results
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing list of results')
    l.exception(e)
    return handle_exc(e, request)

@login_required
#@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin', 'Placement Department')).exists(), login_url=login_url)
def company(request, company_id, year = None) :
  """
  View results of a company for a particular year.
  """
  try :
    if not year :
      year = current_session_year()
    else :
      year = int(year) # the link gives unicode
    l.info(request.user.username + ': Viewing company results for year = ' + str(year) + ', and company = ' + str(company_id))
    company = Company.objects.get(pk = company_id)
    results = Results.objects.filter(company = company)
    session = str(year) + '-' + str(year+1)[2:4]
    return render_to_response('placement/results_view_company.html', {
        'company' : company,
        'session' : session,
        'results' : results
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing list of results for company ' + str(company_id))
    l.exception(e)
    return handle_exc(e, request)

@login_required
#@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin', 'Placement Department')).exists(), login_url=login_url)
def branch(request, branch_code, year = None) :
  """
  View results of a branch for a particular year.
  """
  try :
    if not year :
      year = current_session_year()
    else :
      year = int(year) # link gives year in unicode
    l.info(request.user.username + ': Viewing company results for year = ' + str(year) + ', and branch ' + str(branch_code))
    branch = get_object_or_404(Branch, code = branch_code)
    results = Results.objects.filter(company__year__exact = year, student__branch = branch).order_by('student__user__name')
    degrees = []
    session = str(year) + '-' + str(year+1)[2:4]
    return render_to_response('placement/results_view_branch.html', {
        'branch' : branch,
        'session' : session,
        'results' : results
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing list of results for branch ' + str(branch_code))
    l.exception(e)
    return handle_exc(e, request)

@login_required
#@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin', 'Placement Department')).exists(), login_url=login_url)
def branch_company(request, branch_code, year = None) :
  """
  View results of a branch grouped by company for a particular year.
  """
  try :
    if not year :
      year = current_session_year()
    else :
      year = int(year) # link gives year in unicode
    l.info(request.user.username + ': Viewing results grouped by company results for year = ' + str(year) + ', and branch ' + str(branch_code))
    branch = get_object_or_404(Branch, code = branch_code)
    # TODO : Add an order by
    results = Results.objects.filter(company__year__exact = year, student__branch = branch)\
        .values('company', 'company__name').annotate(placed = Count('company'))
    session = str(year) + '-' + str(year+1)[2:4]
    total_placed = []
    for result in results :
      total_placed.append(Results.objects.filter(company = result['company']).count())
    results = zip(results, total_placed)
    return render_to_response('placement/results_view_branch_company.html', {
        'branch' : branch,
        'session' : session,
        'results' : results
        }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing list of results for branch ' + str(branch_code))
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def declare(request, company_id) :
  """
  Declare results for the company.
  """
  try :
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    l.info(request.user.username + ': Declaring results for ' + str(company_id))
    if request.method == 'POST':
      # set status of selected application to SELECTED
      CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')).update(status='SEL')
      # Can a student be selected for placement in two companies? Ans: a student can be selected in a max of two companies.
      # create entry in Results
      for application in CompanyApplicationMap.objects.filter(pk__in = request.POST.getlist('selected_applications')) :
        plac_person = application.plac_person
        Results.objects.create(student = plac_person.student, company = company)
        # Update PlacementPerson of the persons just placed.
        if plac_person.no_of_companies_placed == 0 :
          plac_person.no_of_companies_placed = 1
          plac_person.placed_company_category = company.category
        else :
          plac_person.no_of_companies_placed += 1
          plac_person.placed_company_category = policy.get_higher_category(plac_person.placed_company_category, company.category)
        plac_person.save()
      l.info(request.user.username + ': Successfully Declared results for ' + str(company_id))
      messages.success(request, 'The marked students are selected for placement in ' + company.name + '.')
      return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
    else :
      applications = CompanyApplicationMap.objects.filter(company = company, status = 'FIN', shortlisted=True)
      return render_to_response('placement/declare_results.html', {
          'company' : company,
          'applications' : applications,
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': Encountered Exception while declaring results for ' + str(company_id))
    l.exception(e)
    return handle_exc(e, request)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def drop(request, company_id) :
  """
  Drop some results from the results that were earlier declared for the company.
  """
  try :
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    l.info(request.user.username + ': Dropping results for ' + str(company_id))
    if request.method == 'POST' :
      # TODO : use transaction to make sure all the queries run properly
      results = Results.objects.filter(pk__in = request.POST.getlist('selected_results'))
      # persons' list for whom the results are to be dropped
      persons = results.values_list('student', flat = True)
      # Update the application to show that the student is not selected in this company
      CompanyApplicationMap.objects.filter(company = company, plac_person__student__in = persons).update(status = 'FIN')
      # Update PlacementPerson of the student.
      for result in results :
        plac_person = PlacementPerson.objects.get(student = result.student)
        if plac_person.no_of_companies_placed == 1 :
          plac_person.no_of_companies_placed = 0
          plac_person.placed_company_category = None
        else :
          plac_person.no_of_companies_placed -= 1
          person_placed = Results.objects.filter(student = plac_person.student)
          # TODO : What if the student was placed in 3 companies? this logic fails to restore the
          # placed_company_category properly. FIXME
          if person_placed[0].company == company :
            old_placed = person_placed[1]
          else :
            old_placed = person_placed[0]
          plac_person.placed_company_category = old_placed.company.category
        plac_person.save()
      # delete the results
      results.delete()
      l.info(request.user.username + ': Successfully dropped results for ' + str(company_id))
      messages.success(request, 'The selected results were dropped successfully.')
      return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
    else :
      # Do not use CompanyApplicationMap to show list of selected students as admin
      # can directly insert results.
      results = Results.objects.filter(company = company)
      # TODO : Convert code to human readable value
      return render_to_response('placement/drop_results.html', {
          'company' : company,
          'results' : results
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': Encountered Exception while dropping results for ' + str(company_id))
    l.exception(e)
    return handle_exc(e, request)

# Departmentwise results start
# Here degree can be UG/PG/PHD
@login_required
#@user_passes_test(lambda u: u.groups.filter(name__in=('Student', 'Placement Admin', 'Placement Department')).exists(), login_url=login_url)
def department(request, year = None, department_id = None, degree = None) :
  """
  Displays the placement results of a department for a particular year. It displays the list of the departments when no
  department is specified. But when a department is specified, it displays the OVERALL results of
  that department. You can specify a degree to view results for that degree only.
  """
  try :
    current_session = current_session_year()
    if year :
      year = int(year)
    else :
      year = current_session
    l.info(request.user.username + ': Viewing department results')
    session = str(year) + '-' + str(year+1)[2:4]
    year_min = Results.objects.aggregate(min = Min('company__year'))['min']
    if year_min == None :
      year_min = current_session
    # years_list for displaying on the top. It is in the form
    # [(2010,'2010-11'), (2011,'2011-12')]
    years_list = []
    for i in range(year_min, current_session):
      years_list.append( (i, str(i) + '-' + str(i+1)[2:4]) )
    if department_id == None :
      # Display a list of departments
      return render_to_response('placement/results/departments_list.html', {
          'year' : year,
          'session' : session,
          'current_year' : current_session,
          'years_list' : years_list,
          'departments' : MC.DEPARTMENT_CHOICES,
          'degrees' : MC.GRADUATION_CHOICES
          }, context_instance = RequestContext(request))
    else :
      if department_id not in zip(*MC.DEPARTMENT_CHOICES)[0] :
        messages.error(request, "Department does not exist")
        return HttpResponseRedirect(reverse('placement.views_results.department'))
      dept_name = [ name for id, name in MC.DEPARTMENT_CHOICES if id == department_id ][0]
      if degree == None :
        # Display overall results of the department
        pp_degree = PlacementPerson.objects.all() # Partially applied filters for degree
        results_degree = Results.objects.all()
        degree = 'Overall'
      else :
        # Display results for a particular degree
        if degree not in zip(*MC.GRADUATION_CHOICES)[0] :
          raise Http404
        pp_degree = PlacementPerson.objects.filter(student__branch__graduation = degree)
        pp_degree = pp_degree.exclude(status='CLS')
        results_degree = Results.objects.filter(student__branch__graduation = degree)
      if year <> current_session:
        passout_year = year + 1
        total_students = pp_degree.filter(student__branch__department = department_id,
                                          student__passout_year = passout_year,
                                          ).count()
      else:
        passout_year = None
        total_students = pp_degree.filter(student__branch__department = department_id,
                                          student__passout_year = passout_year,
                                          status__in = ['OPN', 'LCK', 'VRF'],
                                          ).count()
      registered_students = pp_degree.filter(student__branch__department = department_id,
                                             status = 'VRF',
                                             student__passout_year = passout_year
                                             ).count()
      # TODO : rectify this query as a student may get selected in two companies
      placed_students = results_degree.filter(student__branch__department = department_id,
                                              company__year__exact = year,
                                              student__passout_year = passout_year
                                              ).values('student').distinct().count()
      if registered_students :
        divide_by = registered_students
      else:
        divide_by = 1
      percent_placed = (placed_students*100)/divide_by

      # Calculate AVG CTC
      # Here we cannot use the avg function of django QuerySet 'coz of :
      #    1.  The results are divided into UG/PG/PHD, with each graduation attached to a different pay_package
      #    2.  The ctc is stored in the format : 'amount denomitaion' e.g. '1000 USD'
      total_ctc = 0
      total_count = 0
      for result in results_degree.filter(student__branch__department = department_id,
                                          company__year__exact = year) :
        graduation = result.student.branch.graduation
        package = '' # In the format '1000 USD'
        #package = result.company.__getattribute__('package_'+graduation.lower()) # It's a hack!
        #total_ctc += get_ctc(package)
        total_ctc = 0
        total_count += 1
      if total_count :
        avg_ctc = total_ctc/total_count
      else :
        avg_ctc = 0
      # Pie charts
      pie_charts = []
      sector_dict = {} # stores the dictionary for sectors, e.g. { 'COR' : 'Core', }
      cat_dict = {} # stores the dictionary for categories, e.g. { 'U' : 'University', }
      pie_sector = []
      pie_cat = []
      for sct_id, sct_name in PC.COMPANY_RESUME_CHOICES :
        sector_dict[sct_id] = sct_name
      for cat_id, cat_name in PC.COMPANY_CATEGORY_CHOICES :
        cat_dict[cat_id] = cat_name
      for result in results_degree.filter(company__year__exact = year,
                                          student__branch__department = department_id
                                          ).values('company__sector').annotate(count=Count('company__sector')) :
        pie_sector.append([sector_dict[result['company__sector']], result['count']])
      for result in results_degree.filter(company__year__exact = year,
                                                  student__branch__department = department_id
                                                  ).values('company__category').annotate(count=Count('company__category')) :
        pie_cat.append([cat_dict[result['company__category']], result['count']])
      pie_sector = json.dumps(pie_sector)
      pie_cat = json.dumps(pie_cat)
      pie_placed = "[['Placed', %s], ['Not placed', %s]]" % (placed_students, registered_students-placed_students)
      pie_registered = "[['Registered', %s], ['Unregistered', %s]]" % (registered_students, total_students-registered_students)
      pie_charts.append(('pie_sector', 'Sectorwise Distribution of Results', pie_sector))
      pie_charts.append(('pie_category', 'Categorywise Distribution of Results', pie_cat))
      pie_charts.append(('pie_placed', 'Placed Students', pie_placed))
      pie_charts.append(('pie_registered', 'Registered Students', pie_registered))
      # end of pie charts
      return render_to_response('placement/results/department.html', {
          'dept_code' : department_id,
          'dept_name' : dept_name,
          'year' : year,
          'session' : session,
          'total_students' : total_students,
          'registered_students' : registered_students,
          'placed_students' : placed_students,
          'percent_placed' : percent_placed,
          'avg_ctc' : avg_ctc,
          'degrees_list' : MC.GRADUATION_CHOICES,
          'degree' : degree,
          'pie_charts' : pie_charts
          }, context_instance = RequestContext(request))
  except Exception as e :
    l.info(request.user.username + ': Encountered Exception while viewing results for department')
    l.exception(e)
    return handle_exc(request, e)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Placement Admin').exists(), login_url=login_url)
def insert(request, company_id, branch_code = None) :
  """
  Insert results for the company.
  """
  try :
    l.info(request.user.username + ': Inserting results for ' + str(company_id) )
    company = get_object_or_404(Company, pk = company_id, year = current_session_year() )
    if request.method == 'POST':
      # PlacementPerson.objects.filter(pk__in = request.POST.getlist('selected_students')).update(status='SEL')
      # Can a student be selected for placement in two companies? Ans: a student can be selected in a max of two companies.
      # create entry in Results
      students = PlacementPerson.objects.filter(pk__in = request.POST.getlist('selected_students'))
      for plac_person in students :
        if len(Results.objects.filter(student = plac_person.student, company = company)) != 0:
          continue
        Results.objects.create(student = plac_person.student, company = company)
        # Update PlacementPerson of the persons just placed.
        if plac_person.no_of_companies_placed == 0 :
           plac_person.no_of_companies_placed = 1
           plac_person.placed_company_category = company.category
        else :
           plac_person.no_of_companies_placed += 1
           plac_person.placed_company_category = policy.get_higher_category(plac_person.placed_company_category, company.category)
        plac_person.save()
        l.info(request.user.username + ': Successfully inserted results for ' + str(company_id))
      messages.success(request, 'The marked students are selected for placement in ' + company.name + '.')
      return HttpResponseRedirect(reverse('placement.views_company.admin_list'))
    elif branch_code <> None :
      branch = Branch.objects.get(pk = branch_code)
      student_list = PlacementPerson.objects.filter(student__branch = branch, status = 'VRF', student__passout_year = None).order_by('student__user__name')
      return render_to_response('placement/insert_results.html', {
          'company' : company,
          'student_list' : student_list,
          }, context_instance = RequestContext(request))
    else :
      branches = Branch.objects.all()
      return render_to_response('placement/insert_results.html', {
          'company' : company,
          'branches' : branches,
          }, context_instance = RequestContext(request))
  except Exception as e:
    l.info(request.user.username + ': Encountered Exception while inserting results')
    l.exception(e)
    return handle_exc(e, request)

