import xlrd
from nucleus.models import User , Faculty , Course ,Batch
from lectut.models import Post , Uploadedfile
from lectut.views import getFileType

workbook = xlrd.open_workbook('apps/lectut/scripts/lectures.xlsx')
upload_type = 'lec'
worksheet = workbook.sheet_by_name('Sheet1')

num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row,success,fail,post_id = 0,0,0,0
fail_prof,fail_course = [],[]

while curr_row<num_rows:
  try:
#    import pdb;pdb.set_trace()
    fac_name =  worksheet.cell_value(curr_row , 1)
    course_code = worksheet.cell_value(curr_row , 2)
    file_type_name = worksheet.cell_value(curr_row , 3)
    file_type = getFileType(file_type_name)
    file_name = worksheet.cell_value(curr_row , 4)
    print 'Got values'
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
    course = Course.objects.get(code = course_code)
    batch = Batch.objects.get(course = course)
  except:
    fail +=1
    import pdb;pdb.set_trace()
    print  'Batch issues'
    fail_course.append(course_code)
  try:
    if not Post.objects.filter(batch = batch).exists():
      try:
        content = 'This post contains all previous files in your course'
        new_post = Post(upload_user=user,batch = batch,course = course, content=content, privacy=False)
        new_post.save()
      except:
        fail+=1
        print 'Couldnot create post'
    else:
      new_post = Post.objects.get(batch = batch)
#    fileToAdd = Uploadedfile(post = new_post,upload_file = ,description=,upload_type=upload_type,file_type=file_type)
#    fileToAdd.save()
    print 'Successfully added file'
    success +=1
  except Exception as e:
    fail +=1
    print 'Error in saving file:' +str(e)
  curr_row +=1

print 'Final:'
print 'Success' +str(success)
print 'Fail' +str(fail)
