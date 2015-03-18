from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

from xhtml2pdf import pisa

from mcm.models import MCM, StudentLoanAid
from mcm.forms import MCMForm, StudentLoanAidForm
from mcm.constants import *
from nucleus.models import Student, StudentInfo, Branch
from placement.models import EducationalDetails

import logging, datetime
import cStringIO as StringIO
from django.conf import settings

"""
@login_required
def _mcm_submit(request):
  person = Person.objects.get(user = request.user)
  personinfo, created = PersonInfo.objects.get_or_create(person = person)
  if request.method == 'POST':
    form = McmForm(request.POST)
    mcm_person = McmPerson()
    if form.is_valid():
      person.bhawan = form.cleaned_data['bhawan']
      person.room_no = form.cleaned_data['room_no']
      person.personal_contact_no = form.cleaned_data['mobile_no']
      person.email_id = form.cleaned_data['email']
      person.semester = form.cleaned_data['semester']
      personinfo.fathers_name = form.cleaned_data['fathers_name']
      personinfo.fathers_occupation = form.cleaned_data['fathers_occupation']
      personinfo.permanent_address = form.cleaned_data['home_address']
      personinfo.bank_name = form.cleaned_data['bank_name']
      personinfo.bank_account_no = form.cleaned_data['account_no']
      personinfo.bank_account_no = form.cleaned_data['account_no']
      personinfo.bank_name = form.cleaned_data['bank_name']
      personinfo.category = form.cleaned_data['category']
      mcm_person.air = form.cleaned_data['air']
      mcm_person.unfair_means = form.cleaned_data['unfair_means']
      mcm_person.family_income = form.cleaned_data['family_income']
      mcm_person.other_scholarship = form.cleaned_data['other_scholarship']
      mcm_person.person = person
      mcm_person.date_time = datetime.datetime.now()
      person.save()
      personinfo.save()
      mcm_person.save()
      return HttpResponseRedirect('/thanks/')
  else:
    form = McmForm(initial = {
        'name':person.name,
        'branch':person.branch.code,
        'email':person.email_id,
        'bhawan':person.bhawan,
        'room_no':person.room_no,
        'mobile_no':person.personal_contact_no,
        'graduation':person.branch.graduation,
        'semester':person.semester,
        'fathers_occupation':personinfo.fathers_occupation,
        'fathers_name':personinfo.fathers_name,
        'fathers_occupation':personinfo.fathers_occupation,
        'home_address':personinfo.permanent_address,
        'bank_name':personinfo.bank_name,
        'account_no':personinfo.bank_account_no,
        'category':'personinfo.category'})
  return render_to_response('mcm/mcm_registration.html', {'form' : form}, context_instance=RequestContext(request))
"""

# This is to check user permissons
#NOTE: This permission set is according to session 2014-15, so do update this accordingly in future.
def check_permission(user, scholarship_type):
  if user.in_group('Student'):
    try:
      student = Student.objects.get(user=user)
      if student:
        allowed_degrees_FreeMessing = ['B.Tech.', 'B.Arch.', 'IDD', 'IMT', 'IMSc', 'MCA', 'MBA', 'MSc']
        allowed_degrees_MCM = ['B.Tech.', 'B.Arch.', 'IDD', 'IMT', 'IMSc', 'MCA', 'MSc']
        allowed_degrees = []
        if scholarship_type == 'MCM':
          allowed_degrees = allowed_degrees_MCM
        elif scholarship_type == 'FreeMessing':
          allowed_degrees = allowed_degrees_FreeMessing
        else:
          return False

        if student.branch.degree in allowed_degrees:
          return True
        elif student.branch.degree == 'M.Tech.' and student.branch.department == 'ESD':
          return True
        else:
          return False
      else:
        return False
    except:
      return False
      pass
  else:
    return False

@login_required
def loan_aid_submit(request):
  if not check_permission(request.user, 'FreeMessing'):
    messages.info(request,"'Student Loan Aid Form' for Free Messing is not open for your department. Please contact 'IMG' in case of any discrepency")
    return HttpResponseRedirect('/')
  person = Student.objects.get(user = request.user)
  studentinfo, created = StudentInfo.objects.get_or_create(student=person)
  if StudentLoanAid.objects.filter(student=person).exists():
    student = StudentLoanAid.objects.filter(student=person)[0]
  else:
    student = StudentLoanAid.objects.create(student=person)

  if request.method == 'POST':
    form = StudentLoanAidForm(request.POST)
    string = ''
    if 'other-scholarship-detail' in request.POST:
      for scholarship in request.POST.getlist('other-scholarship-detail'):
        if string and scholarship:
          string = string + ", " + scholarship
        elif scholarship:
          string = scholarship
    if form.is_valid():
      form.process()
      student.guardians_name = form.cleaned_data['guardians_name']
      student.guardians_occupation = form.cleaned_data['guardians_occupation']
      student.guardians_income = form.cleaned_data['guardians_income']
      student.guardians_address = form.cleaned_data['guardians_address']
      student.mothers_income = form.cleaned_data['mothers_income']
      student.fathers_income = form.cleaned_data['fathers_income']
      student.other_scholarship_details = string
      student.previous_aid_amount = form.cleaned_data['previous_aid_amount']
      student.previous_aid_session = form.cleaned_data['previous_aid_session']
      student.work_bhawan_details = form.cleaned_data['work_bhawan_details']
      student.mothers_pan_no = form.cleaned_data['mothers_pan_no']
      student.mothers_occupation = form.cleaned_data['mothers_occupation']
      student.fathers_pan_no = form.cleaned_data['fathers_pan_no']
      student.guardians_pan_no = form.cleaned_data['guardians_pan_no']
      student.sgpa = form.cleaned_data['sgpa']
      student.cgpa = form.cleaned_data['cgpa']
      student.date_time = datetime.datetime.now()
      student.check = True
      student.save()
      template_name = 'mcm/loan_aid_pdf.html'
      studentinfo, created = StudentInfo.objects.get_or_create(student = person)
      return render_to_response('mcm/la_success.html',
      context_instance = RequestContext(request))
      """
      html = render_to_string(template_name, {
            'person' : person,
            'form_personinfo' : personinfo,
            'studentloanaid' : student,
            'date': datetime.datetime.now()},
            context_instance = RequestContext(request))
      result = StringIO.StringIO()
      def fetch_resources(uri, rel):
        return os.path.join(settings.PROJECT_ROOT, 'static',
            uri.replace(settings.STATIC_URL, ''))
      pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
      result = result.getvalue()
      response = HttpResponse(result, content_type='application/pdf')
      response['Content-Disposition'] = ('attachment; filename=SALFForm_' + person.user.username
          + '_' + str(datetime.datetime.now()).replace(' ','-').replace(':','-') +'.pdf')
      response['Content-Length'] = len(result)
      return response
      """
  else:
    try:
      person_course = get_prev_sem(person.semester)
      student_edu_info = EducationalDetails.objects.get(student=person, course=person_course)
      sgpa = student_edu_info.sgpa
      cgpa = student_edu_info.cgpa
    except Exception as e:
      sgpa = "0.0"
      cgpa = "0.0"
      print e
      pass

    form = StudentLoanAidForm(initial = {
        'name': person.user.name,
        'enroll_no': person.user.username,
        'cgpa' : cgpa,
        'sgpa': sgpa,
        'branch': person.branch.name,
        'graduation': person.branch.degree,
        'bhawan': person.bhawan,
        'room_no': person.room_no,
        'semester': person.get_semester_display(),
        'fathers_occupation': studentinfo.fathers_occupation,
        'fathers_name': studentinfo.fathers_name,
        'home_address': studentinfo.permanent_address,
        'bank_name': studentinfo.bank_name,
        'account_no': studentinfo.bank_account_no,
        'category': studentinfo.get_category_display(),
        'bank_name': studentinfo.bank_name,
        'account_no': studentinfo.bank_account_no,
        'room_no': person.room_no,
        })
  return render_to_response('mcm/student_loan.html',
      {'form' : form, 'student': student},
      context_instance = RequestContext(request))

@login_required
def print_pdf(request):
  if not check_permission(request.user, 'FreeMessing'):
    messages.info(request,"'Student Loan Aid Form' for Free Messing is not open for your department. Please contact 'IMG' in case of any discrepency")
    return HttpResponseRedirect('/')
  person = Person.objects.get(user = request.user)
  student = StudentLoanAid.objects.filter(student = person)[0]
  personinfo, created = StudentInfo.objects.get_or_create(student = person)
  template_name = 'mcm/loan_aid_pdf.html'
  print str(student.guardians_address) + str(student.guardians_income)
  html = render_to_string(template_name, {
        'person' : person,
        'form_personinfo' : personinfo,
        'studentloanaid' : student,
        'date': datetime.datetime.now()},
        context_instance = RequestContext(request))
  result = StringIO.StringIO()
  def fetch_resources(uri, rel):
    return os.path.join(settings.PROJECT_ROOT, 'static',
        uri.replace(settings.STATIC_URL, ''))
  pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
  result = result.getvalue()
  response = HttpResponse(result, content_type='application/pdf')
  response['Content-Disposition'] = ('attachment; filename=SALFForm_' + person.user.username
      + '_' + str(datetime.datetime.now()).replace(' ','-').replace(':','-') +'.pdf')
  response['Content-Length'] = len(result)
  return response

def get_prev_sem(sem):
  sem_no = sem[len(sem) - 1]
  year_no = sem[len(sem) - 2]
  sem_no = int(sem_no)
  year_no = int(year_no)
  if sem_no == 0:
    year_no = year_no - 1
  sem_no = 1 - sem_no
  sem = sem[:-2]
  return sem + str(year_no) + str(sem_no)

@login_required
def mcm_submit(request):
  if not check_permission(request.user, 'FreeMessing'):
    messages.info(request,"MCM Scholarship is not open for your department. Please contact 'IMG' in case of any discrepency")
    return HttpResponseRedirect('/')
  person = Student.objects.get(user = request.user)
  personinfo, created = StudentInfo.objects.get_or_create(student = person)

  if MCM.objects.filter(student = person).exists():
    student = MCM.objects.filter(student = person)[0]
    """
    ### Temporary code block. Note: Please remove this while reopening this portal ###
    if student.check is False:
      messages.info(request,"MCM and Free-messing Scholarship portal is closed now! Please contact 'IMG' in case of any discrepency")
      return HttpResponseRedirect('/')
    ##### Ends
    """
  else:
    """
    ### Temporary code block. Note: Please remove this while reopening this portal ###
    messages.info(request,"MCM and Free-messing Scholarship portal is closed now! Please contact 'IMG' in case of any discrepency")
    return HttpResponseRedirect('/')
    ##### Ends
    """
    student = MCM.objects.create(student = person)

  if request.method == 'POST':
    form = MCMForm(request.POST)
    string = ''
    if 'other-scholarship-detail' in request.POST:
      for scholarship in request.POST.getlist('other-scholarship-detail'):
        if string and scholarship:
          string = string + ", " + scholarship
        elif scholarship:
          string = scholarship
    if form.is_valid():
      form.process()
      student.other_scholarship_details = string
      student.sgpa = form.cleaned_data['sgpa']
      student.cgpa = form.cleaned_data['cgpa']
      student.air = form.cleaned_data['air']
      student.unfair_means = form.cleaned_data['unfair_means']
      student.family_income = form.cleaned_data['family_income']
      student.scholar_type = form.cleaned_data['scholar_type']
      student.payment_choice = form.cleaned_data['payment_choice']
      print 'here'
      scholtype=form.cleaned_data['scholar_type']
      flag=0
      p=form.cleaned_data['payment_choice']
      pay_choice=""
      print scholtype
      title="Merit-Cum-Means (MCM) Scholarship"
      if scholtype=="MCM":
        if person.branch.degree is 'MBA':   # Hard coded - Raw degree check.
          messages.info(request,"MCM Scholarship is not open for your department. Please contact 'IMG' in case of any discrepency")
          return HttpResponseRedirect('/')
        title="Merit-Cum-Means (MCM) Scholarship"
      elif scholtype=="GIS":
        title="Institute Scholarship (SC/ST)"
        flag=1
        if p=="SCHOL":
          pay_choice="For Scholarship of Rs. 1000/- per month for 10 months."
        elif p=="MESS":
          pay_choice="Free Messing (basic menu only) with Rs. 250/- per month for 10 months, as per allowance."
      student.check = True
      student.save()
      person.bhawan = form.cleaned_data['bhawan']
      person.room_no = form.cleaned_data['room_no']
      person.personal_contact_no = form.cleaned_data['mobile_no']
      person.email_id = form.cleaned_data['email']
      personinfo.fathers_name = form.cleaned_data['fathers_name']
      personinfo.fathers_occupation = form.cleaned_data['fathers_occupation']
      personinfo.permanent_address = form.cleaned_data['home_address']
      personinfo.bank_name = form.cleaned_data['bank_name']
      personinfo.bank_account_no = form.cleaned_data['account_no']
      person.save()
      personinfo.save()
      #template_name = 'mcm/mcm_pdf.html'
      personinfo, created = StudentInfo.objects.get_or_create(student = person)
      return render_to_response('mcm/mcm_success.html',
      context_instance = RequestContext(request))

      """
      html = render_to_string(template_name, {
            'person' : person,
            'form_personinfo' : personinfo,
            'student' : student,
            'title':title,
            'date': datetime.datetime.now(),
            'flag':flag,
            'pay_choice':pay_choice,},
            context_instance = RequestContext(request))
      result = StringIO.StringIO()
      def fetch_resources(uri, rel):
        return os.path.join(settings.PROJECT_ROOT, 'static',
            uri.replace(settings.STATIC_URL, ''))
      pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
      result = result.getvalue()
      response = HttpResponse(result, content_type='application/pdf')
      response['Content-Disposition'] = ('attachment; filename=MCM_' + person.user.username
      + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") +'.pdf')
      response['Content-Length'] = len(result)
      return response
      """
  else:
    sgpa = "0.0"
    cgpa = "0.0"
    try:
      #person_course = get_prev_sem(person.semester)
      #student_info = EducationalDetails.objects.get(person=person, course=person_course)
      student_info = EducationalDetails.objects.filter(student = person, course__startswith = person.branch.graduation).order_by('-course')[0]
      sgpa = student_info.sgpa
      cgpa = student_info.cgpa
    except Exception as e:
      sgpa = "0.0"
      cgpa = "0.0"
      print e
      pass

    form = MCMForm(initial = {
        'name': person.user.name,
        'enroll_no': person.user.username,
        'cgpa' : cgpa,
        'sgpa': sgpa,
        'branch': person.branch.name,
        'graduation': person.branch.degree,
        'bhawan': person.bhawan,
        'room_no': person.room_no,
        'semester': person.get_semester_display(),
        'fathers_occupation': personinfo.fathers_occupation,
        'fathers_name': personinfo.fathers_name,
        'home_address': personinfo.permanent_address,
        'category': personinfo.get_category_display(),
        'bank_name': personinfo.bank_name,
        'account_no': personinfo.bank_account_no,
        'room_no': person.room_no,
        'mobile_no': person.user.contact_no,
        'email': person.user.email,
        })
  return render_to_response('mcm/mcm.html',
      {'form' : form, 'student': student},
      context_instance = RequestContext(request))

@login_required
def mcm_print_pdf(request):
  if not check_permission(request.user, 'FreeMessing'):
    messages.info(request,"MCM Scholarship is not open for your department. Please contact 'IMG' in case of any discrepency")
    return HttpResponseRedirect('/')
  person = Student.objects.get(user = request.user)
  student = MCM.objects.filter(student = person)[0]
  scholtype=student.scholar_type
  p=student.payment_choice
  title=""
  flag=0
  pay_choice=""
  title="Merit-Cum_Means (MCM) Scholarship"
  if scholtype=="MCM":
    title="Merit-Cum-Means (MCM) Scholarship"
  elif scholtype=="GIS":
    title="Institute Scholarship (SC/ST)"
    flag=1
    if p=="SCHOL":
      pay_choice="For Scholarship of Rs. 1000/- per month for 10 months."
    elif p=="MESS":
      pay_choice="Free Messing (basic menu only) with Rs. 250/- per month for 10 months, as per allowance."
  personinfo, created = StudentInfo.objects.get_or_create(student = person)
  template_name = 'mcm/mcm_pdf.html'
  html = render_to_string(template_name, {
        'person' : person,
        'form_personinfo' : personinfo,
        'student' : student,
        'title':title,
        'flag':flag,
        'pay_choice':pay_choice,
        'date': datetime.datetime.now()},
        context_instance = RequestContext(request))
  result = StringIO.StringIO()
#  import pdb; pdb.set_trace()
  def fetch_resources(uri, rel):
    return os.path.join(settings.PROJECT_ROOT, 'static',
        uri.replace(settings.STATIC_URL, ''))
  pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('utf8')), result)
  result = result.getvalue()
  response = HttpResponse(result, content_type='application/pdf')
  response['Content-Disposition'] = ('attachment; filename=MCM_' + person.user.username
      + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M") +'.pdf')
  response['Content-Length'] = len(result)
  return response

@login_required
@user_passes_test(lambda u: u.groups.filter(name = 'Acads Admin').exists())
def scholarship_data_listing(request):
  MCM = ['B.Tech.', 'B.Arch.', 'IDD', 'IMT', 'IMSc', 'MCA', 'MSc', 'M.Tech.']
  FreeMessing = ['B.Tech.', 'B.Arch.', 'IDD', 'IMT', 'IMSc', 'MCA', 'MBA', 'MSc', 'M.Tech.']
  return render_to_response('mcm/scholarship_data_listing.html',
    {'MCM':MCM, 'FreeMessing':FreeMessing},
    context_instance = RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name = 'Acads Admin').exists())
def download_scholarship_data(request):
  degree = request.GET.get('degree')
  scholarship_type = request.GET.get('scholarship_type')
  persons = MCM.objects.filter(scholar_type = scholarship_type, student__branch__degree = degree, check = True, datetime__gt=datetime.date(2014,8,1))
  persons = persons.order_by('person__branch__code')
  departments = persons.values_list('person__branch').distinct()

  dept_no=0
  department_sorted = [[] for i in range(len(departments))]
  for per in persons:
    dept = str(departments[dept_no]).split("'")[1]
    if per.student.branch.code == dept:
      department_sorted[dept_no].append(per)
    else :
      dept_no+=1
      department_sorted[dept_no].append(per)
  dept_no=0
  for arr in department_sorted:
    department_sorted[dept_no] = sorted(arr, key=lambda mcm_obj:mcm_obj.person.semester)
    dept_no+=1

  import xlwt
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet(str(scholarship_type)+str(degree))
  response = HttpResponse(content_type='application/ms-excel')
  response['Content-Disposition'] = 'attachment; filename = scholarship_' + scholarship_type + '_' + degree + '.xls'
  row_num = 0
  columns = [
    (u"Enrollment No.", 5000),
    (u"Name", 8000),
    (u"Branch Name", 10000),
    (u"Branch Code", 3500),
    (u"Semester", 3000),
    (u"AIR", 2000),
    (u"CGPA", 2000),
    (u"SGPA", 2000),
    (u"Family Income", 4000),
    (u"Payment Choice", 8000),
    (u"Bank Name", 8000),
    (u"Bank Account Number", 8000),
    (u"Unfair Means",3500)
  ]

  font_style = xlwt.XFStyle()
  font_style.font.bold = True

  for col_num in xrange(len(columns)):
    ws.write(row_num, col_num, columns[col_num][0], font_style)
    ws.col(col_num).width = columns[col_num][1]

  font_style = xlwt.XFStyle()
  font_style.alignment.wrap = 1

  for arr in department_sorted:
    for mcm_obj in arr:
      row_num+=1
      person_info = StudentInfo.objects.get(student=mcm_obj.person)
      if mcm_obj.unfair_means == True:
        uf = "Yes"
      else :
        uf = "No"
      row = [
        mcm_obj.person.user.username,
        mcm_obj.person.user.name,
        mcm_obj.person.branch.name,
        mcm_obj.person.branch.code,
        mcm_obj.person.semester,
        mcm_obj.air,
        mcm_obj.cgpa,
        mcm_obj.sgpa,
        mcm_obj.family_income,
        mcm_obj.payment_choice,
        person_info.bank_name,
        person_info.bank_account_no,
        uf
      ]

      for col_num in xrange(len(row)):
        ws.write(row_num, col_num, row[col_num], font_style)

  wb.save(response)
  return response
  export_xls.short_description = u"Export XLS"
