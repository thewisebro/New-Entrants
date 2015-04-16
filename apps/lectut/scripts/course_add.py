#!/usr/bin/python
'''
import os, sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django.conf.settings")
from django.conf import settings
'''
import xlrd
import logging
from nucleus.models import Course

workbook = xlrd.open_workbook('apps/lectut/scripts/courses_all.xlsx')
worksheet = workbook.sheet_by_name('Sheet1')


num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0
print num_rows
print num_cells
success_counter = 0
fail_counter = 0

while curr_row < num_rows:
  code = worksheet.cell_value(curr_row , 0)
  name = worksheet.cell_value(curr_row , 1)
  credits = worksheet.cell_value(curr_row , 2)
  try:
    course = Course(code = code , name = name , credits = credits , subject_area = 'Default', semtype = 'S' , year = 2015)
    course.save()
    success_counter +=1
  except Exception as e:
    print str(curr_row)+' Error here'+str(e)
    logging.warning('Line number: '+str(curr_row)+' Course code: '+str(code))
    fail_counter +=1

  curr_row +=1

print 'Final Tally:'
print 'Success ' + str(success_counter)
print 'Fail ' + str(fail_counter)
