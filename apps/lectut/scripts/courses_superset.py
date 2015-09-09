''' This file deals with merging courses as available in nucleus and regol and making a superset out of it '''

from nucleus.models import Course
from regol.models import CourseDetails

import xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet('Extra')
row = 2

nucleus_courses = Course.objects.all()
regol_courses = CourseDetails.objects.all()
count = 0
course_names = []

for r_course in regol_courses:
  check = 0
  for n_course in nucleus_courses:
    if r_course.course_code == n_course.code:
      check = 1
  if check ==0:
    count = count+1
    ws.write(row,2,r_course.course_name)
    row = row+1
    course_names.append(r_course.course_name)

wb.save('extra.xls')
print 'Count = '+str(count)
print course_names

