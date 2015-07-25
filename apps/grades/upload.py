#!/usr/bin/python
import os, sys
sys.path.append(os.getcwd())
import settings
from django.core.management import setup_environ
setup_environ(settings)

import xlrd
from os import listdir
from nucleus.models import *
from regol.models import *
from grades.models import *


def transfer_to_database(way,file_xls):
  path = way+'/'+str(file_xls)
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
    enrollment_no = int(worksheet.cell_value(curr_row,1))
    try:
      student = Student.objects.get(user__username = enrollment_no)
      course_code = str(file_xls).split('.')[0]
      course = CourseDetails.objects.get(course_code = course_code)
      registered_courses = RegisteredCourses.objects.filter(student=student,course_details=course)[0]
      semester = registered_courses.semester
      if semester == "A":
        semester = student.semester
      grade = worksheet.cell_value(curr_row,6)
      obj = Grade.objects.get_or_create(student=student,course=course)[0]
      obj.semester = semester
      obj.course = course
      obj.grade = grade
      obj.save()
    except Exception as e:
      print 'Escaped following student : '+str(enrollment_no)+" error : "+str(e)
      pass



path = os.path.join(os.path.dirname(__file__),'uploads')
for count,file_xls in enumerate(listdir(path)):
  transfer_to_database(path,file_xls)
  print str(count+1)+'/'+str(len(listdir(path)))+' uploaded'
