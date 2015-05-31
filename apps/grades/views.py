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
    course_details.append(str(course.course_details.course_code) + " - " + (course.course_details.course_name.upper()))
    obj = Grade.objects.filter(student=student,course = course.course_details)
    if obj:
      grades.append(obj[0].grade)
      try:
        marks_scored = marks_scored + course.credits*int(GRADE_CHOICES[obj[0].grade])
      except ValueError:
        pass
      sum_of_credits = sum_of_credits + course.credits
    else:
      grade_exists = False
      grades.append('-')
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
