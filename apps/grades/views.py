from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from grades.models import *
from nucleus.models import Student
from regol.models import RegisteredCourses
from django.contrib.auth.models import User
from django.template import RequestContext
from grades import forms
from grades.constants import *
import xlrd

#@login_required
#def upload(request):
#  student = request.user.student
#  user = request.user
#  if user.in_group('IMG Admin'):
#    form = forms.UploadForm()
#    if request.method == 'POST':
#      form = forms.UploadForm(request.POST,request.FILES)
#      print form
#      if form.is_valid():
#        File = request.FILES['data']
#        semester = request.POST['semester']
#        form.save()
#        transfer_to_database(File,semester)
#        return HttpResponse('Successfully Uploaded')
#      else:
#        return HttpResponse('Successfully asd')
#    else:
#      msg = 'Welcome Admin'
#      return render_to_response('grades/upload.html',{
#          'form' : form,
#          'msg' : msg,
#          },context_instance = RequestContext(request))
#  else:
#    return HttpResponse("Admin only!!")

@login_required
def index(request):
  student = request.user.student
  user = request.user
  courses = RegisteredCourses.objects.filter(student=student,cleared_status = "CUR")
  course_details = []
  is_admin = False
  grade_exists = True
  sum_of_credits = 0
  marks_scored = 0
  if user.in_group('IMG Admin'):
    is_admin = True
  grades = []
  for course in courses:
    code1 = course.course_details.course_code.split('-')[0][:2]
    code2 = ''
    if len(course.course_details.course_code.split('-'))==2:
      code2 = course.course_details.course_code.split('-')[1]
    obj = Grade.objects.filter(student=student,course__course_code = code1+'-'+code2)
    objn = Grade.objects.filter(student=student,course__course_code = code1+'N-'+code2)
    if not obj and objn:
      obj = objn

    course_details.append(str(course.course_details.course_code) + " : " + (course.course_details.course_name.upper()))

    if obj:
      grades.append(obj[0].grade)
      try:
        marks_scored = marks_scored + course.credits*int(GRADE_CHOICES[obj[0].grade])
        sum_of_credits = sum_of_credits + course.credits
      except ValueError:
        pass
    else:
      grade_exists = False
      grades.append('-')
  disp = CourseDetails.objects.get(course_code='DISP')
  course_details.append(str(disp.course_code) + " : " + (disp.course_name.upper()))
  obj = Grade.objects.filter(student=student,course = disp)
  if obj:
    grades.append(obj[0].grade)
    try:
      marks_scored = marks_scored + course.credits*int(GRADE_CHOICES[obj[0].grade])
      sum_of_credits = sum_of_credits + course.credits
    except ValueError:
      pass
  grades = zip(course_details,grades)
  if grade_exists and sum_of_credits!=0:
    sgpa = round(float(marks_scored)/float(sum_of_credits),2)
  else:
    sgpa = None
  return render_to_response('grades/index.html',{
      'grades' : grades,
      'is_admin':is_admin,
      'grade_exists':grade_exists,
      'sgpa':sgpa,
      },context_instance = RequestContext(request))



def transfer_to_database(File,semester):
  path = 'media/grades/'+str(File._name)
  workbook = xlrd.open_workbook(path)
  worksheet = workbook.sheet_by_index(0)
  num_rows = worksheet.nrows - 1
  num_cells = worksheet.ncols - 1
  curr_row = 0
  check = True
  while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    curr_cell = -1
    while check:
      while curr_cell < num_cells:
        curr_cell += 1
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        if cell_value.startswith('Enr'):
          check = False
      curr_row+=1
      curr_cell = -1
    enrollment_no = worksheet.cell_value(curr_row,1)
    try:
      person = Person.objects.get(user__username = enrollment_no)
      course_code = str(File._name).split('.')[0]
      course = CourseDetails.objects.get(course_code = course_code)
      grade = worksheet.cell_value(curr_row,6)
      obj = Grade.objects.get_or_create(person = person,course=course)[0]
      obj.course = course
      obj.semester = semester
      obj.grade = grade
      obj.save()
    except:
      print 'Escaped following person : '+str(enrollment_no)
      pass
