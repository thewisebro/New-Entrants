''' File to transfer old files from old_files_lectut/ in the lectut/ directory'''

import xlrd
import os
import shutil
import xlwt

from nucleus.models import *

file_types = ['exp','lec','tut','sol']
os.chdir('media/old_files_lectut')

for file_type in file_types:
  print os.getcwd()
  workbook = xlrd.open_workbook("../../apps/lectut/scripts/old_db/"+file_type+".xlsx")   # Change individually for each type (exams,lectures,solutions,tutorials)
  worksheet = workbook.sheet_by_name('Sheet1')
  num_rows = worksheet.nrows-1
  os.chdir(file_type)                      # change depending upon workbook file
  curr_dir = os.getcwd()
  ls=os.listdir(curr_dir)
  print ls
  fail,total_files,total_fac,total_success = 0,0,0,0

  total_fac = len(ls)

  wb = xlwt.Workbook(encoding='latin-1')
  ws = wb.add_sheet('Errors')
  row = 5

  ws.write(1,1,'Total Files')
  ws.write(2,1,'Total Faculty')
  ws.write(2,2,total_fac)
  ws.write(3,1,'Total_Success')
  ws.write(4,1,'Total_fail')

  for each_chu in ls:
    os.chdir(each_chu)
    file_list=os.listdir(os.getcwd())#abhi faculty k andar hu main
#  print file_list
    total_files = total_files + len(file_list)
    for each_file in file_list:
      curr_row = 1
      checker = 0
      while curr_row<num_rows:
        if each_file == worksheet.cell_value(curr_row,3):
          checker = 1
          try:
            course = worksheet.cell_value(curr_row,2)
            extension=each_file.split('.')[-1]
#         topic = worksheet.cell_value(curr_row,4)
#          fullname=topic + '.' + extension
            direc_type=None
            if extension in ['jpg','png','jpeg','gif','exif','tiff']:
              directype='image'
            elif extension in ['pdf']:
              directype='pdf'
            elif extension in ['ppt', 'pptx' , 'pot','pptm','potx','potm','ppsx']:
              directype="ppt"
            elif extension in ['dv', 'mov', 'mp4', 'avi', 'wmv', 'mkv', 'webm']:
              directype='video'
            elif extension in ['gz','tar','iso','lbr','zip']:
              directype='zip'
            elif extension.startswith('xl') or extension in ['ods']:
              directype='sheet'
            elif extension in ['xlsx','xlsv','xls','ods']:
              directype="sheet"
            elif extension in ['doc','docx','odt','rtf']:
              directype="doc"
            else:
              directype='other'
            directory = '../../../lectut/'+course+'/'+directype+'/'
            if not os.path.exists(directory):
              os.makedirs(directory)
            shutil.copy2(each_file,directory)
            new_course_code = ''
            if len(course.split('-')[0])==2:
              new_course_code = course.split('-')[0]+'N'
              new_course_code += '-'+course.split('-')[1]
        

            if len(course.split('-')[0])==3:
              new_course_code = course.split('-')[0][:2]
              new_course_code += '-'+course.split('-')[1]

            c1 = Course.objects.filter(code = new_course_code)
            if len(c1) == 1:
              print new_course_code
              course2 = c1[0].code
              directory = '../../../lectut/'+course2+'/'+directype+'/'
              if not os.path.exists(directory):
                os.makedirs(directory)
              shutil.copy2(each_file,directory)
              total_success = total_success+1

            print 'Copied file : ' +str(each_file)
            total_success = total_success+1
          except Exception as e:
            ws.write(row,2,str(each_file))
            ws.write(row,3,str(e))
            row=row+1
            print 'Some error' +str(e)
            fail+=1
          curr_row = num_rows
        curr_row +=1
      if checker == 0:
        ws.write(row,2,each_file)
        ws.write(row,3,'Couldnot find file in document')
        print 'Could not find file ' + str(each_file)
        row = row+1
        fail+=1
    os.chdir('../')
  os.chdir('../')

  ws.write(1,2,total_files)
  ws.write(3,2,total_success)
  ws.write(4,2,fail)
  wb.save('files_error_'+file_type+'.xlsx')
  print fail
