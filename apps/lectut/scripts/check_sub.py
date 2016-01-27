''' To check if the given course list exists in our DB '''


import xlrd
import os
import shutil
import xlwt
from nucleus.models import Course

new = []
workbook = xlrd.open_workbook("apps/lectut/scripts/subject.xlsx")
worksheet = workbook.sheet_by_name('Sheet2')
num_rows = worksheet.nrows-1
for i in range(num_rows):
  name = worksheet.cell_value(i,3)
  print name
  if not Course.objects.filter(code = name).exists():
    if name not in new:
      print str(name)+' : Course not found'
      new.append(name)

print new
print 'Total:'+str(len(new))
