''' Add students to batches from XLSX file '''

import xlrd
import os
import shutil
import xlwt
from nucleus.models import *

remove,add = 0,0
curr_stud = '12117027'
workbook = xlrd.open_workbook("/home/harshit/channeli/apps/lectut/scripts/subject.xlsx")
worksheet = workbook.sheet_by_name('Sheet2')
num_rows = worksheet.nrows-1

wb = xlwt.Workbook(encoding='latin-1')
ws = wb.add_sheet('Student_errors')
row = 3

ws.write(1,1,'Enrollment Number')
ws.write(1,2,'Course')
ws.write(1,3,'Error')

for i in range(num_rows):
  try:
    stud = worksheet.cell_value(i,0)
    code = worksheet.cell_value(i,3)
#    import pdb;pdb.set_trace()
    if curr_stud != stud:
      curr_stud = stud
      user = User.objects.get(username = stud)
      student = user.student
      batches = student.batch_set.all()
      batch_ids = map(lambda x: x.id,batches)
      print batch_ids

    course = Course.objects.get(code = code)
    batch = Batch.objects.get(course = course)
    if batch.id in batch_ids:
      remove+=1
      batch.students.remove(student)
      batch_ids.remove(batch.id)
    else:
      batch.students.add(student)
      add+=1
  except Exception as e:
    ws.write(row,1,stud)
    ws.write(row,2,code)
    ws.write(row,3,str(e))
    row+=1
    print e


print 'Removed'+str(remove)
print 'Added'+str(add)
wb.save('Student_add_errors.xlsx')
