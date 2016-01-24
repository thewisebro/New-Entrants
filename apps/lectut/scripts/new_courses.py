''' This file is used to create new courses and make their repositories '''

from nucleus.models import Course
import os
import xlrd
import xlwt

os.chdir('media/lectut')
workbook = xlrd.open_workbook("apps/lectut/scripts/subject.xlsx")
worksheet = workbook.sheet_by_name('Sheet2')
num_rows = worksheet.nrows-1

wb = xlwt.Workbook()
ws = wb.add_sheet('Courses')
row = 2
success,fail = 0,0

ws.write(1,1,'Course Code')
ws.write(1,2,'Course Name')
ws.write(1,3,'Error')


for i in range(num_rows):
  code = worksheet.cell_value(i,3)
  if not Course.objects.filter(code = code).exists():
    try:
      name = worksheet.cell_value(i,4)
      credits = worksheet.cell_value(i,6)
      courseToAdd = Course(code = code, name = name, credits = credits, year = 2016)
      courseToAdd.save()
      os.mkdir(course.code)
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
      success+=1
    except Exception as e:
      fail+=1
      row = row+1
      ws.write(row,1,code)
      ws.write(row,2,name)
      ws.write(row,3,str(e))
      print str(e)

wb.save('new_course_errors.xlsx')
print 'Courses Added :'+str(success)
print 'Fail :'+str(fail)
