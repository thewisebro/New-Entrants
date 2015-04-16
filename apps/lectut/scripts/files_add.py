import xlrd
import os
from django.core.files.base import File
from nucleus.models import User , Faculty , Course ,Batch
from lectut.models import Post , Uploadedfile
from lectut.views import getFileType

workbook = xlrd.open_workbook('apps/lectut/scripts/lectures.xlsx')
upload_type = 'lec'
worksheet = workbook.sheet_by_name('Sheet1')

os.chdir('media/lectut/amain')
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row,success,fail,post_id,file_saves = 1,0,0,0,0
fail_prof,fail_course = [],[]
change_dir = False

while curr_row<num_rows:
  try:
    fac_name =  worksheet.cell_value(curr_row , 1)
    course_code = worksheet.cell_value(curr_row , 2)
    file_type_name = worksheet.cell_value(curr_row , 3)
    file_type = getFileType(file_type_name)
    file_name = worksheet.cell_value(curr_row , 4)
    filename = file_name+'.'+file_type_name.split('.')[1]
    print 'Got values'
#    import pdb;pdb.set_trace()
  except:
    print 'Some value missing at ' + str(curr_row)
  try:
    user = User.objects.get(username = fac_name)
    faculty = user.faculty
    success +=1
  except:
    fail +=1
    fail_prof.append(fac_name)
  try:
#    import pdb;pdb.set_trace()
    course = Course.objects.get(code = course_code)
    batch = Batch.objects.get(course = course)
  except:
    fail +=1
    print  'Batch issues'
    batch = []
    fail_course.append(course_code)
  if batch:
    try:
      os.chdir(batch.name)
      os.chdir('other')
      change_dir = True
    except:
      pass
    try:
      if not Post.objects.filter(course = course).exists():
        try:
          content = 'This post contains all previously uploaded files in your course'
          new_post = Post(upload_user=user,batch = batch,course = course, content=content, privacy=False)
          new_post.save()
        except:
          fail+=1
          print 'Couldnot create post'
      else:
        new_post = Post.objects.get(batch = batch)
#      import pdb;pdb.set_trace()    
      file_object = open(filename)
#      file_object = File(filename)    
      fileToAdd = Uploadedfile(post = new_post, upload_file = File(file_object), description=filename,upload_type=upload_type,file_type=file_type)
      fileToAdd.save()
      print 'Successfully added file'
      file_saves +=1
      success +=1
    except Exception as e:
      fail +=1
      print 'Error in saving file:' +str(e)
  if change_dir:
    change_dir = False
    os.chdir('../../')
  curr_row +=1

print 'Final:'
print 'Success' +str(success)
print 'Fail' +str(fail)
print file_saves
