import xlrd
import xlwt
import os
from django.core.files.base import File
from nucleus.models import User , Faculty , Course ,Batch
from lectut.models import Post , Uploadedfile
from lectut.views import getFileType

os.chdir('media/lectut')
upload_types=['lec','tut','sol','exp']

for upload_type in upload_types:
  workbook = xlrd.open_workbook('/home/apps/channeli/apps/lectut/scripts/old_db/'+upload_type+'.xlsx')
  worksheet = workbook.sheet_by_name('Sheet1')

  num_rows = worksheet.nrows - 1
  num_cells = worksheet.ncols - 1
  curr_row,success,fail,post_id,file_saves = 1,0,0,0,0
  fail_prof,fail_course = [],[]
  change_dir,progress = False,True

  wb= xlwt.Workbook(encoding='latin-1')
  ws = wb.add_sheet('Errors')
  row = 5

  while curr_row<num_rows:
    try:
      fac_name =  worksheet.cell_value(curr_row , 1)
      course_code = worksheet.cell_value(curr_row , 2)
      filename = worksheet.cell_value(curr_row , 3)
      file_type = getFileType(filename)
      file_name = worksheet.cell_value(curr_row , 4)
#      filename = file_name+'.'+file_type_name.split('.')[1]
      print 'Got values for file:'+str(file_name)
    except:
      print 'Some value missing at ' + str(curr_row)
      ws.write(row,2,str(curr_row))
      ws.write(row,3,str(file_name))
      ws.write(row,4,'Missing values in xlsx')
      row +=1

    try:
      user = User.objects.get(username = fac_name)
      faculty = user.faculty
      success +=1
    except:
      fail +=1
      progress = False
      ws.write(row,2,str(curr_row))
      ws.write(row,3,str(file_name))
      ws.write(row,4,'Couldnot find faculty')
      row+=1

    try:
#      import pdb;pdb.set_trace()
      course = Course.objects.get(code = course_code)
      batch = Batch.objects.get(course = course)
      os.chdir(course_code)
      os.chdir(file_type)
      change_dir = True
    except:
      fail +=1
      print  'Batch issues'
      progress = False
      ws.write(row,2,str(curr_row))
      ws.write(row,3,str(course_code))
      ws.write(row,4,'Couldnot find Batch/Course')
      row+=1

    if progress:
      try:
        if not Post.objects.filter(course = course).filter(upload_user=user).exists():
          try:
            content = 'This post contains all previously uploaded files in your course'
            new_post = Post(upload_user=user,batch = batch,course = course, content=content, privacy=False)
            new_post.save()
          except:
            fail+=1
            print 'Couldnot create post'
        else:
          new_post = Post.objects.get(batch = batch, upload_user = user)
        file_object = open(filename)
#      file_object = File(filename)    
        fileToAdd = Uploadedfile(post = new_post, upload_file = File(file_object), description=filename,upload_type=upload_type,file_type=file_type)
        fileToAdd.save()
        print 'Successfully added file:'+str(filename)
        file_saves +=1
      except Exception as e:
        fail +=1
        print 'Error in saving file:' +str(e)
        ws.write(row,2,str(curr_row))
        ws.write(row,3,str(filename))
        ws.write(row,4,'Couldnot save file :'+str(e))
        row+=1
      print 'old',course.code
      new_course_code = ''
      if len(course.code.split('-')[0])==2:
        new_course_code = course.code.split('-')[0]+'N'
        new_course_code += '-'+course.code.split('-')[1]
        

      if len(course.code.split('-')[0])==3:
        new_course_code = course.code.split('-')[0][:2]
        new_course_code += '-'+course.code.split('-')[1]

      c1 = Course.objects.filter(code = new_course_code)
      if len(c1) == 1:
        course = c1[0]
        batch = Batch.objects.get(course=course) 
        print new_course_code
        print course
        print batch
        print user
        print Post.objects.filter(course = course).filter(upload_user=user)
        try:
          if not Post.objects.filter(course = course).filter(upload_user=user).exists():
            try:
              content = 'This post contains all previously uploaded files in your course'
              new_post = Post(upload_user=user,batch = batch,course = course, content=content, privacy=False)
              print '\t',
              print batch
              new_post.save()
            except:
              fail+=1
              print 'Couldnot create post'
          else:
            new_post = Post.objects.filter(course=course, upload_user = user)[0]
          print new_post
          print new_post.course
          file_object = open(filename)
#        file_object = File(filename)    
          fileToAdd = Uploadedfile(post = new_post, upload_file = File(file_object), description=filename,upload_type=upload_type,file_type=file_type)
          fileToAdd.save()
          print 'Successfully added file:'+str(filename)
          file_saves +=1
        except Exception as e:
          fail +=1
          print 'Error in saving file:' +str(e)
          ws.write(row,2,str(curr_row))
          ws.write(row,3,str(filename))
          ws.write(row,4,'Couldnot save file :'+str(e))
          row+=1
 
    else:
      print ' Some error in retrieving values'
      progress = True

    if change_dir:
      change_dir = False
      os.chdir('../../')
    curr_row +=1

  print 'Final:'
  print 'Success' +str(success)
  print 'Fail' +str(fail)
  print file_saves

wb.save('files_db_errors.xlsx') 
