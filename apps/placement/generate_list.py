import xlwt
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'apache.override'

from placement.models import *

workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('Details')
r = 0
worksheet.write(0, 0, label = 'Sno')
worksheet.write(0, 1, label = 'Department')
worksheet.write(0, 2, label = 'Branch')
worksheet.write(0, 3, label = 'Enrollment No')
worksheet.write(0, 4, label = 'Name')
worksheet.write(0, 5, label = 'Year')
worksheet.write(0, 6, label = 'CGPA')

p = PlacementPerson.objects.filter(person__passout_year = None, status__in = ['OPN', 'LCK', 'VRF'])

for x in p:
  r += 1
  worksheet.write(r, 0, label = str(r))
  worksheet.write(r, 1, label = x.person.branch.get_department_display())
  worksheet.write(r, 2, label = x.person.branch.name)
  worksheet.write(r, 3, label = x.person.user.username)
  worksheet.write(r, 4, label = x.person.name)
  try:
    worksheet.write(r, 5, label = str(2014 - int(x.person.admission_year)))
  except:
    worksheet.write(r, 5, label = '-')
  worksheet.write(r, 6, label = x.person.cgpa)
workbook.save('placement-data.xls')
