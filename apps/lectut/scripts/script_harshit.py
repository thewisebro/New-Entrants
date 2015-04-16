import xlrd
import os
import shutil

print os.getcwd()
workbook = xlrd.open_workbook("lectut_port/tutorials.xlsx")          # Change individually for each type (exams,lectures,solutions,tutorials)
worksheet = workbook.sheet_by_name('Sheet1')
num_rows = worksheet.nrows-1
os.chdir('../uploads/tutorials')                      # change depending upon workbook file
curr_dir = os.getcwd()
ls=os.listdir(curr_dir)
print ls
fail = 0

for each_chu in ls:
  os.chdir(each_chu)
  file_list=os.listdir(os.getcwd())#abhi faculty k andar hu main
#  print file_list
  for each_file in file_list:
    curr_row = 1
    while curr_row<num_rows:
      if each_file == worksheet.cell_value(curr_row,3):
        try:
          course = worksheet.cell_value(curr_row,2)
          course+=':2015S'
          extension=each_file.split('.')[1]
          topic = worksheet.cell_value(curr_row,4)
          fullname=topic + '.' + extension
          direc_type=None
          if extension in ['jpg','png','jpeg','gif','exif','tiff']:
            directype='image'
          if extension in ['pdf']:
              directype='pdf'
          if extension in ['dv', 'mov', 'mp4', 'avi', 'wmv', 'mkv', 'webm']:
            directype='video'
          if extension in ['gz','tar','iso','lbr','zip']:
            directype='zip'
          if extension.startswith('xl') or extension in ['ods']:
            directype='sheet'
          else:
            directype='other'
          shutil.copy2(each_file,'../../../lectut_work/amain/'+course+'/'+directype+'/'+fullname)
          print 'Copied file ' +str(fullname)
        except Exception as e:
          print 'Some error' +str(e)
          fail+=1
      curr_row +=1
  os.chdir('../')
os.chdir('../../lectut_work')

print fail
