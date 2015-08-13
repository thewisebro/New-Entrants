''' This file is used to make repositories of respective courses '''

from nucleus.models import Course
import os
import xlrd
import xlwt

os.chdir('media/lectut')
courses = Course.objects.all()
success_count = 0
fail_count = 0

wb = xlwt.Workbook()
ws = wb.add_sheet('Courses')
row = 2

ws.write(1,1,'Course Code')
ws.write(1,2,'Course Name')
ws.write(1,3,'Error')


for course in courses:
  try:
#    import pdb;pdb.set_trace()
    os.mkdir(course.code)
    success_count = success_count+1
    os.chdir(course.code)
    os.mkdir('image')
    os.mkdir('video')
    os.mkdir('ppt')
    os.mkdir('pdf')
    os.mkdir('zip')
    os.mkdir('doc')
    os.mkdir('sheet')
    os.mkdir('other')
    os.chdir('../')
  except Exception as e:
    fail_count = fail_count+1
    row = row+1
    ws.write(row,1,course.code)
    ws.write(row,2,course.name)
    ws.write(row,3,str(e))

wb.save('course_folder_errors.xlsx')

print 'Success : '+ str(success_count)
print 'Fail : ' + str(fail_count)
